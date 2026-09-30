"""
Goal & Achievement service — progress tracking and auto-unlock logic.
"""

from datetime import date
from typing import Optional, Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.models.social import Achievement, UserAchievement
from app.models.fitness import BMIRecord
from app.repositories.steps_repository import StepsRepository
from app.repositories.workout_repository import WorkoutRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.utils.calculations import calculate_bmi, bmi_category, calculate_bmr, calculate_tdee, calculate_age, calculate_goal_progress


class GoalService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.goal_repo = GoalRepository(db)
        self.user_repo = UserRepository(db)

    async def calculate_bmi(self, user_id: int, weight_kg: float, height_cm: float) -> dict:
        """Calculate BMI/BMR/TDEE and save to history."""
        user = await self.user_repo.get_with_profile(user_id)
        profile = user.profile if user else None

        bmi_val = calculate_bmi(weight_kg, height_cm)
        category = bmi_category(bmi_val)

        # Calculate BMR/TDEE if we have age/gender
        bmr_val = None
        tdee_val = None
        if profile and profile.date_of_birth and profile.gender:
            age = calculate_age(profile.date_of_birth)
            bmr_val = calculate_bmr(weight_kg, height_cm, age, profile.gender)
            activity = profile.activity_level or "moderate"
            tdee_val = calculate_tdee(bmr_val, activity)

        # Save record
        record = await self.goal_repo.create_bmi_record(
            user_id=user_id,
            weight_kg=weight_kg,
            height_cm=height_cm,
            bmi=bmi_val,
            category=category,
            bmr=bmr_val,
            tdee=tdee_val,
        )

        # Update profile weight
        if profile:
            await self.user_repo.update_profile(user_id, weight_kg=weight_kg, height_cm=height_cm)

        return {
            "bmi": bmi_val,
            "category": category,
            "bmr": bmr_val,
            "tdee": tdee_val,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "disclaimer": "These values are estimates for informational purposes. Consult a healthcare professional for medical advice.",
        }

    async def get_bmi_history(self, user_id: int) -> list[dict]:
        records = await self.goal_repo.get_bmi_history(user_id)
        return [
            {
                "date": r.date.isoformat(),
                "weight_kg": r.weight_kg,
                "bmi": r.bmi,
                "category": r.category,
                "bmr": r.bmr,
                "tdee": r.tdee,
            }
            for r in records
        ]

    async def get_weight_progress(self, user_id: int) -> dict:
        """Track weight goal progress."""
        user = await self.user_repo.get_with_profile(user_id)
        profile = user.profile if user else None
        if not profile or not profile.weight_kg or not profile.target_weight_kg:
            return {"progress": 0, "message": "Set your target weight to track progress"}

        # Get first recorded weight
        records = await self.goal_repo.get_bmi_history(user_id, limit=100)
        if not records:
            return {"progress": 0, "current": profile.weight_kg, "target": profile.target_weight_kg}

        start_weight = records[-1].weight_kg  # Oldest record
        current_weight = profile.weight_kg
        target_weight = profile.target_weight_kg
        progress = calculate_goal_progress(start_weight, current_weight, target_weight)

        return {
            "start_weight": start_weight,
            "current_weight": current_weight,
            "target_weight": target_weight,
            "progress_percent": progress,
            "remaining_kg": round(abs(current_weight - target_weight), 1),
        }


class AchievementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_achievements(self) -> list[dict]:
        result = await self.db.execute(
            select(Achievement).where(Achievement.is_active == True).order_by(Achievement.category)
        )
        return [
            {
                "id": a.id,
                "name": a.name,
                "description": a.description,
                "category": a.category,
                "icon": a.icon,
                "badge_color": a.badge_color,
                "requirement_value": a.requirement_value,
                "xp_reward": a.xp_reward,
            }
            for a in result.scalars().all()
        ]

    async def get_user_achievements(self, user_id: int) -> list[dict]:
        result = await self.db.execute(
            select(UserAchievement)
            .where(UserAchievement.user_id == user_id, UserAchievement.is_completed == True)
            .order_by(UserAchievement.earned_at.desc())
        )
        earned = result.scalars().all()
        achievements = []
        for ua in earned:
            # Load achievement details
            ach_result = await self.db.execute(
                select(Achievement).where(Achievement.id == ua.achievement_id)
            )
            ach = ach_result.scalar_one_or_none()
            if ach:
                achievements.append({
                    "id": ach.id,
                    "name": ach.name,
                    "description": ach.description,
                    "category": ach.category,
                    "icon": ach.icon,
                    "badge_color": ach.badge_color,
                    "earned_at": ua.earned_at.isoformat() if ua.earned_at else None,
                })
        return achievements

    async def check_and_award(self, user_id: int, category: str, value: float) -> list[str]:
        """Check if user qualifies for any new achievements. Returns list of newly earned names."""
        result = await self.db.execute(
            select(Achievement).where(
                Achievement.is_active == True,
                Achievement.category == category,
                Achievement.requirement_value <= value,
            )
        )
        candidates = result.scalars().all()
        newly_earned = []

        for ach in candidates:
            # Check if already earned
            existing = await self.db.execute(
                select(UserAchievement).where(
                    UserAchievement.user_id == user_id,
                    UserAchievement.achievement_id == ach.id,
                    UserAchievement.is_completed == True,
                )
            )
            if existing.scalar_one_or_none():
                continue

            # Award it
            ua = UserAchievement(
                user_id=user_id,
                achievement_id=ach.id,
                earned_at=datetime.now(timezone.utc),
                progress=100.0,
                is_completed=True,
            )
            self.db.add(ua)
            newly_earned.append(ach.name)

        if newly_earned:
            await self.db.flush()
        return newly_earned
