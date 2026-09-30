"""
Models package - imports all models so Alembic can detect them.
"""
from app.models.user import User, UserProfile, UserSettings
from app.models.auth import AuthToken, OTPCode, PasswordReset
from app.models.fitness import (
    StepsDaily, StepsHourly, CalorieLog, WaterLog,
    BMIRecord, BodyMeasurement, ProgressPhoto,
)
from app.models.nutrition import Food, FoodImage, NutritionData, Meal, MealItem
from app.models.workout import (
    Exercise, ExerciseVideo, ExerciseMuscle,
    WorkoutPlan, WorkoutPlanExercise, WorkoutSession, WorkoutSessionExercise,
)
from app.models.social import (
    Achievement, UserAchievement, Challenge, UserChallenge,
    Notification, Device, DeviceSyncData,
)
from app.models.ai import AIPrediction, AIChatHistory
from app.models.admin import AdminLog, AuditLog

__all__ = [
    "User", "UserProfile", "UserSettings",
    "AuthToken", "OTPCode", "PasswordReset",
    "StepsDaily", "StepsHourly", "CalorieLog", "WaterLog",
    "BMIRecord", "BodyMeasurement", "ProgressPhoto",
    "Food", "FoodImage", "NutritionData", "Meal", "MealItem",
    "Exercise", "ExerciseVideo", "ExerciseMuscle",
    "WorkoutPlan", "WorkoutPlanExercise", "WorkoutSession", "WorkoutSessionExercise",
    "Achievement", "UserAchievement", "Challenge", "UserChallenge",
    "Notification", "Device", "DeviceSyncData",
    "AIPrediction", "AIChatHistory",
    "AdminLog", "AuditLog",
]
