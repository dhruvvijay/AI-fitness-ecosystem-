"""
Tests for fitness calculation utilities.
"""

import pytest
from app.utils.calculations import (
    calculate_bmi, bmi_category, calculate_bmr, calculate_tdee,
    calculate_target_calories, calculate_macros, calculate_water_goal_ml,
    steps_to_distance_km, steps_to_calories, exercise_calories_burned,
    calculate_goal_progress,
)


class TestBMI:
    def test_normal_bmi(self):
        bmi = calculate_bmi(70, 175)
        assert 22 < bmi < 24

    def test_underweight(self):
        bmi = calculate_bmi(45, 170)
        assert bmi_category(bmi) == "underweight"

    def test_normal(self):
        bmi = calculate_bmi(65, 170)
        assert bmi_category(bmi) == "normal"

    def test_overweight(self):
        bmi = calculate_bmi(85, 170)
        assert bmi_category(bmi) == "overweight"

    def test_obese(self):
        bmi = calculate_bmi(110, 170)
        assert bmi_category(bmi) == "obese"


class TestBMR:
    def test_male_bmr(self):
        bmr = calculate_bmr(75, 175, 30, "male")
        assert 1650 < bmr < 1750

    def test_female_bmr(self):
        bmr = calculate_bmr(60, 165, 25, "female")
        assert 1300 < bmr < 1500

    def test_female_lower_than_male(self):
        male = calculate_bmr(70, 170, 30, "male")
        female = calculate_bmr(70, 170, 30, "female")
        assert female < male


class TestTDEE:
    def test_sedentary(self):
        tdee = calculate_tdee(1700, "sedentary")
        assert tdee == 2040

    def test_active(self):
        tdee = calculate_tdee(1700, "active")
        assert tdee == 2932

    def test_unknown_defaults_moderate(self):
        tdee = calculate_tdee(1700, "unknown_level")
        assert tdee == 2635


class TestTargetCalories:
    def test_lose_weight(self):
        target = calculate_target_calories(2500, "lose_weight")
        assert target == 2000  # 20% deficit

    def test_gain_muscle(self):
        target = calculate_target_calories(2500, "gain_muscle")
        assert target == 2750  # 10% surplus

    def test_maintain(self):
        target = calculate_target_calories(2500, "maintain")
        assert target == 2500

    def test_minimum_floor(self):
        target = calculate_target_calories(1000, "lose_weight")
        assert target >= 1200  # Safety floor


class TestMacros:
    def test_macros_sum_to_target(self):
        macros = calculate_macros(2200, 75, "maintain")
        total_cal = macros["protein_g"] * 4 + macros["carbs_g"] * 4 + macros["fat_g"] * 9
        # Allow 10% tolerance due to rounding
        assert abs(total_cal - 2200) < 220

    def test_higher_protein_for_muscle_gain(self):
        maintain = calculate_macros(2500, 75, "maintain")
        gain = calculate_macros(2500, 75, "gain_muscle")
        assert gain["protein_g"] > maintain["protein_g"]


class TestSteps:
    def test_distance_reasonable(self):
        distance = steps_to_distance_km(10000, 175)
        assert 6 < distance < 9  # ~7km for 10k steps

    def test_calories_reasonable(self):
        calories = steps_to_calories(10000, 75)
        assert 300 < calories < 500

    def test_zero_steps(self):
        assert steps_to_distance_km(0, 170) == 0
        assert steps_to_calories(0, 70) == 0


class TestExerciseCalories:
    def test_running(self):
        # 30 min running (MET ~10) for 70kg person
        cals = exercise_calories_burned(10.0, 70, 30)
        assert 300 < cals < 400

    def test_walking(self):
        # 30 min walking (MET ~3.5)
        cals = exercise_calories_burned(3.5, 70, 30)
        assert 100 < cals < 150


class TestGoalProgress:
    def test_halfway(self):
        progress = calculate_goal_progress(80, 75, 70)
        assert progress == 50.0

    def test_complete(self):
        progress = calculate_goal_progress(80, 70, 70)
        assert progress == 100.0

    def test_no_change(self):
        progress = calculate_goal_progress(75, 75, 75)
        assert progress == 100.0

    def test_over_target(self):
        progress = calculate_goal_progress(80, 65, 70)
        assert progress == 100.0  # Capped at 100
