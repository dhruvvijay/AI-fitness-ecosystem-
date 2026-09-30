"""
Fitness calculation engine: BMR, TDEE, BMI, macros, body composition.
All formulas use evidence-based equations (Mifflin-St Jeor, Katch-McArdle).
"""

from typing import Optional


class FitnessCalculator:
    """Core fitness and nutrition calculation service."""

    # Activity level multipliers (Mifflin-St Jeor TDEE factors)
    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,       # Little/no exercise
        "light": 1.375,         # 1-3 days/week
        "moderate": 1.55,       # 3-5 days/week
        "active": 1.725,        # 6-7 days/week
        "very_active": 1.9,     # Intense daily + physical job
    }

    def calculate_bmi(self, weight_kg: float, height_cm: float) -> float:
        """Calculate Body Mass Index."""
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)

    def get_bmi_category(self, bmi: float) -> str:
        """Classify BMI into WHO categories."""
        if bmi < 16:
            return "severely_underweight"
        elif bmi < 18.5:
            return "underweight"
        elif bmi < 25:
            return "normal"
        elif bmi < 30:
            return "overweight"
        elif bmi < 35:
            return "obese_class_1"
        elif bmi < 40:
            return "obese_class_2"
        else:
            return "obese_class_3"

    def get_healthy_weight_range(self, height_cm: float) -> dict:
        """Calculate healthy weight range (BMI 18.5–24.9)."""
        height_m = height_cm / 100
        return {
            "min_kg": round(18.5 * (height_m ** 2), 1),
            "max_kg": round(24.9 * (height_m ** 2), 1),
        }

    def calculate_ideal_weight(self, height_cm: float, gender: str) -> float:
        """Calculate ideal body weight using the Devine formula."""
        height_inches = height_cm / 2.54
        base_height = 60  # 5 feet in inches

        if gender == "male":
            ideal = 50 + 2.3 * max(0, height_inches - base_height)
        else:
            ideal = 45.5 + 2.3 * max(0, height_inches - base_height)

        return ideal

    def calculate_bmr(
        self,
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: str,
        body_fat: Optional[float] = None,
    ) -> float:
        """
        Calculate Basal Metabolic Rate.
        Uses Katch-McArdle if body fat is available, otherwise Mifflin-St Jeor.
        """
        if body_fat is not None:
            # Katch-McArdle (more accurate with body fat data)
            lean_mass = weight_kg * (1 - body_fat / 100)
            return 370 + (21.6 * lean_mass)

        # Mifflin-St Jeor (most accurate without body fat)
        if gender == "male":
            return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    def calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure."""
        multiplier = self.ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
        return bmr * multiplier

    def get_recommended_calories(self, tdee: float, goal: str) -> float:
        """Calculate recommended daily calories based on fitness goal."""
        adjustments = {
            "lose_weight": -500,     # ~0.45 kg/week loss
            "maintain": 0,
            "gain_muscle": 300,      # Lean bulk
            "improve_fitness": -200, # Slight deficit for recomposition
        }
        return tdee + adjustments.get(goal, 0)

    def calculate_macros(
        self,
        calories: float,
        weight_kg: float,
        goal: str,
    ) -> dict:
        """
        Calculate macronutrient distribution based on goal.
        Returns grams of protein, carbs, and fat.
        """
        # Protein: 1.6-2.2g per kg for muscle gain, 1.2-1.6g for weight loss
        if goal == "gain_muscle":
            protein_g = weight_kg * 2.0
        elif goal == "lose_weight":
            protein_g = weight_kg * 1.8  # Higher protein preserves muscle during deficit
        else:
            protein_g = weight_kg * 1.6

        protein_cal = protein_g * 4
        remaining_cal = calories - protein_cal

        # Fat: 25-30% of total calories
        if goal == "lose_weight":
            fat_pct = 0.25
        elif goal == "gain_muscle":
            fat_pct = 0.25
        else:
            fat_pct = 0.30

        fat_cal = calories * fat_pct
        fat_g = fat_cal / 9

        # Carbs: remaining calories
        carbs_cal = remaining_cal - fat_cal
        carbs_g = max(0, carbs_cal / 4)

        return {
            "protein": protein_g,
            "carbs": carbs_g,
            "fat": fat_g,
        }

    def calculate_water_intake(self, weight_kg: float, activity_level: str) -> int:
        """Calculate recommended daily water intake in ml."""
        # Base: 35ml per kg body weight
        base_ml = weight_kg * 35

        # Add for activity
        activity_bonus = {
            "sedentary": 0,
            "light": 300,
            "moderate": 500,
            "active": 700,
            "very_active": 1000,
        }

        total = base_ml + activity_bonus.get(activity_level, 500)
        return int(round(total / 100) * 100)  # Round to nearest 100ml

    def get_recommended_goal(self, bmi: float) -> str:
        """Suggest a fitness goal based on current BMI."""
        if bmi < 18.5:
            return "gain_muscle"
        elif bmi < 25:
            return "maintain"
        elif bmi < 30:
            return "lose_weight"
        else:
            return "lose_weight"

    def calculate_body_fat_navy(
        self,
        waist_cm: float,
        neck_cm: float,
        height_cm: float,
        hip_cm: Optional[float] = None,
        gender: str = "male",
    ) -> float:
        """Estimate body fat % using the U.S. Navy method."""
        import math

        if gender == "male":
            bf = 495 / (
                1.0324 - 0.19077 * math.log10(waist_cm - neck_cm) + 0.15456 * math.log10(height_cm)
            ) - 450
        else:
            if hip_cm is None:
                hip_cm = waist_cm * 1.1  # Rough estimate
            bf = 495 / (
                1.29579 - 0.35004 * math.log10(waist_cm + hip_cm - neck_cm) + 0.22100 * math.log10(height_cm)
            ) - 450

        return max(3, min(60, bf))

    def estimate_calories_from_steps(self, steps: int, weight_kg: float = 70) -> float:
        """Estimate calories burned from step count."""
        # ~0.04 calories per step per kg of body weight / 70kg baseline
        return steps * 0.04 * (weight_kg / 70)

    def predict_weight(
        self,
        current_weight: float,
        daily_deficit: float,
        days: int,
    ) -> list[dict]:
        """
        Predict future weight based on calorie deficit.
        1 kg of fat ≈ 7,700 calories.
        """
        predictions = []
        weight = current_weight

        for day in range(1, days + 1):
            weight_change = daily_deficit / 7700  # kg per day
            weight -= weight_change
            weight = max(30, weight)  # Safety floor

            if day % 7 == 0 or day == days:  # Weekly predictions
                predictions.append({
                    "day": day,
                    "week": day // 7,
                    "predicted_weight": round(weight, 1),
                    "total_change": round(current_weight - weight, 1),
                })

        return predictions
