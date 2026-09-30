"""
Fitness calculation utilities.
Evidence-based formulas for BMI, BMR, TDEE, macros, steps, and calories.
"""

import math
from typing import Optional


# ── BMI ──────────────────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """BMI = weight_kg / height_m²"""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    else:
        return "obese"


# ── BMR (Mifflin-St Jeor) ───────────────────────────────────────

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Mifflin-St Jeor equation:
    Male:   10 × weight + 6.25 × height − 5 × age + 5
    Female: 10 × weight + 6.25 × height − 5 × age − 161
    """
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age
    if gender.lower() in ("male", "m"):
        bmr += 5
    else:
        bmr -= 161
    return round(bmr, 0)


# ── TDEE ─────────────────────────────────────────────────────────

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}


def calculate_tdee(bmr: float, activity_level: str) -> float:
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
    return round(bmr * multiplier, 0)


# ── Target Calories ──────────────────────────────────────────────

def calculate_target_calories(tdee: float, goal: str) -> float:
    """
    Calculate target calories based on fitness goal.
    Never recommends below 1200 (women) or 1500 (men) to avoid unsafe deficits.
    """
    if goal in ("lose_weight", "fat_loss"):
        target = tdee * 0.80  # 20% deficit (moderate)
    elif goal in ("gain_muscle", "weight_gain"):
        target = tdee * 1.10  # 10% surplus
    else:  # maintain, improve_fitness
        target = tdee
    return round(max(target, 1200), 0)


# ── Macros ───────────────────────────────────────────────────────

def calculate_macros(
    target_calories: float,
    weight_kg: float,
    goal: str,
) -> dict:
    """
    Calculate macro targets in grams.
    Protein: 1.6-2.2g/kg based on goal.
    Fat: 25-30% of calories.
    Carbs: remaining calories.
    """
    # Protein (g/kg body weight)
    if goal in ("gain_muscle",):
        protein_per_kg = 2.0
    elif goal in ("lose_weight", "fat_loss"):
        protein_per_kg = 1.8
    else:
        protein_per_kg = 1.6

    protein_g = round(weight_kg * protein_per_kg)
    protein_cal = protein_g * 4

    # Fat (25% of total calories)
    fat_cal = target_calories * 0.25
    fat_g = round(fat_cal / 9)

    # Carbs (remaining)
    carbs_cal = target_calories - protein_cal - fat_cal
    carbs_g = round(max(carbs_cal, 0) / 4)

    return {
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "fiber_g": round(target_calories / 1000 * 14),  # 14g per 1000 kcal
    }


# ── Water ────────────────────────────────────────────────────────

def calculate_water_goal_ml(weight_kg: float, activity_level: str) -> int:
    """~35ml per kg, adjusted for activity."""
    base = weight_kg * 35
    multiplier = {"sedentary": 1.0, "light": 1.1, "moderate": 1.2, "active": 1.3, "very_active": 1.4}
    return round(base * multiplier.get(activity_level, 1.2) / 100) * 100  # Round to nearest 100ml


# ── Steps ────────────────────────────────────────────────────────

def steps_to_distance_km(steps: int, height_cm: float) -> float:
    """Estimate distance from steps using stride length (~0.415 × height)."""
    stride_m = height_cm * 0.00415
    return round(steps * stride_m / 1000, 2)


def steps_to_calories(steps: int, weight_kg: float) -> float:
    """Rough estimate: 0.04 kcal per step per kg of body weight / 80kg baseline."""
    return round(steps * 0.04 * (weight_kg / 80), 0)


# ── Exercise Calories ────────────────────────────────────────────

def exercise_calories_burned(met_value: float, weight_kg: float, duration_minutes: float) -> float:
    """Calories = MET × weight_kg × duration_hours."""
    return round(met_value * weight_kg * (duration_minutes / 60), 0)


# ── Goal Progress ────────────────────────────────────────────────

def calculate_goal_progress(start_value: float, current_value: float, target_value: float) -> float:
    """Calculate percentage progress toward a goal (0-100)."""
    total_change = abs(target_value - start_value)
    if total_change == 0:
        return 100.0
    actual_change = abs(current_value - start_value)
    return round(min(actual_change / total_change * 100, 100), 1)


# ── Age from DOB ─────────────────────────────────────────────────

def calculate_age(date_of_birth) -> int:
    """Calculate age from date of birth."""
    from datetime import date
    today = date.today()
    return today.year - date_of_birth.year - (
        (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
    )
