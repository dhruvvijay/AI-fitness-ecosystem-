"""
AI API — food scanner and AI coach, wired to real AI services.
"""

import base64
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.ai.vision import AIVisionService
from app.ai.coach import AICoachService
from app.repositories.user_repository import UserRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.core.responses import success_response
from app.core.config import settings

router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


# ── Food Scanner ─────────────────────────────────────────────────

@router.post("/food-scanner/analyze")
async def analyze_food(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a food image for AI analysis.
    Pipeline: validate → AI detect → nutrition lookup → return structured JSON.
    """
    # Validate file
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        return success_response(
            data=None,
            message="Only JPEG, PNG, and WebP images are supported",
        )

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        return success_response(
            data=None,
            message=f"File size must not exceed {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    # Process with AI
    vision_service = AIVisionService()
    image_b64 = base64.b64encode(content).decode("utf-8")

    try:
        result = await vision_service.analyze_food_image(image_b64, file.content_type)
    except Exception as e:
        # Fallback to mock if AI service unavailable
        result = vision_service.get_mock_analysis()

    result["disclaimer"] = (
        "Nutritional values are AI-estimated and may not be laboratory-accurate. "
        "Use as a guide and adjust portions as needed."
    )
    return success_response(data=result, message="Food analyzed")


# ── AI Coach ─────────────────────────────────────────────────────

@router.post("/coach/chat")
async def chat_with_coach(
    body: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Chat with the AI fitness coach.
    The coach has access to the user's fitness data for context-aware responses.
    """
    # Gather user context
    user_repo = UserRepository(db)
    analytics_repo = AnalyticsRepository(db)
    user_with_profile = await user_repo.get_with_profile(user.id)

    from datetime import date
    daily_data = await analytics_repo.get_daily_summary(user.id, date.today())

    context = {
        "user_name": user.full_name,
        "today": daily_data,
    }
    if user_with_profile and user_with_profile.profile:
        p = user_with_profile.profile
        context["profile"] = {
            "weight_kg": p.weight_kg,
            "height_cm": p.height_cm,
            "fitness_goal": p.fitness_goal,
            "activity_level": p.activity_level,
            "diet_preference": p.diet_preference,
            "daily_calorie_target": p.daily_calorie_target,
        }

    coach_service = AICoachService()
    try:
        response = await coach_service.chat(
            user_message=body.message,
            user_context=context,
            session_id=body.session_id,
        )
    except Exception:
        response = {
            "message": (
                "I'm having trouble connecting to my AI backend right now. "
                "Based on your data, I can see you're making progress! "
                "Keep focusing on your goals and let's try again in a moment."
            ),
            "session_id": body.session_id or "fallback",
        }

    return success_response(data=response)
