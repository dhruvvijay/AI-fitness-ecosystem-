"""
Input validators for the fitness application.
Rejects impossible or unsafe values before they reach the database.
"""

from datetime import date, datetime
from typing import Optional

from app.core.exceptions import ValidationException


def validate_weight(weight_kg: float, field: str = "weight") -> float:
    if weight_kg < 20 or weight_kg > 500:
        raise ValidationException(f"{field} must be between 20 and 500 kg")
    return round(weight_kg, 1)


def validate_height(height_cm: float) -> float:
    if height_cm < 50 or height_cm > 300:
        raise ValidationException("Height must be between 50 and 300 cm")
    return round(height_cm, 1)


def validate_age(age: int) -> int:
    if age < 13 or age > 120:
        raise ValidationException("Age must be between 13 and 120 years")
    return age


def validate_calories(calories: float, field: str = "calories") -> float:
    if calories < 0 or calories > 50000:
        raise ValidationException(f"{field} must be between 0 and 50,000")
    return round(calories, 1)


def validate_steps(steps: int) -> int:
    if steps < 0 or steps > 200000:
        raise ValidationException("Steps must be between 0 and 200,000")
    return steps


def validate_date_not_future(d: date, field: str = "date") -> date:
    if d > date.today():
        raise ValidationException(f"{field} cannot be in the future")
    return d


def validate_gender(gender: str) -> str:
    valid = ("male", "female", "other")
    if gender.lower() not in valid:
        raise ValidationException(f"Gender must be one of: {', '.join(valid)}")
    return gender.lower()


def validate_activity_level(level: str) -> str:
    valid = ("sedentary", "light", "moderate", "active", "very_active")
    if level not in valid:
        raise ValidationException(f"Activity level must be one of: {', '.join(valid)}")
    return level


def validate_file_upload(content_type: str, size_bytes: int, max_mb: int = 10) -> None:
    """Validate uploaded file type and size."""
    allowed = ("image/jpeg", "image/png", "image/webp")
    if content_type not in allowed:
        raise ValidationException(f"File type must be one of: {', '.join(allowed)}")
    max_bytes = max_mb * 1024 * 1024
    if size_bytes > max_bytes:
        raise ValidationException(f"File size must not exceed {max_mb}MB")


def validate_pagination(page: int, limit: int) -> tuple[int, int]:
    """Clamp pagination params to safe ranges."""
    page = max(1, page)
    limit = max(1, min(limit, 100))
    return page, limit
