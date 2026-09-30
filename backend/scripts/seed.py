"""
Database seed script — populates realistic sample data.
Run: python -m scripts.seed
Requires: MySQL running with ai_fitness_db created.
"""

import asyncio
import sys
import os
from datetime import date, timedelta, datetime, timezone
import random

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.db.base import async_session_factory, engine, Base
from app.core.security import hash_password
from app.models.user import User, UserProfile, UserSettings
from app.models.fitness import StepsDaily, CalorieLog, WaterLog, BMIRecord, BodyMeasurement
from app.models.nutrition import Food, Meal, MealItem
from app.models.workout import Exercise, WorkoutPlan, WorkoutSession, WorkoutSessionExercise
from app.models.social import Achievement, UserAchievement, Notification, Device
from app.models.ai import AIChatHistory


# ═══════════════════════════════════════════════════════════════
# FOOD DATABASE — 120+ Indian & International Foods
# ═══════════════════════════════════════════════════════════════

FOODS = [
    # ── Indian Main Course ───────────────────────────────────
    {"name": "White Rice (Cooked)", "category": "grain", "calories": 130, "protein_g": 2.7, "carbs_g": 28, "fat_g": 0.3, "fiber_g": 0.4, "serving_size": "1 cup", "serving_weight_g": 158},
    {"name": "Brown Rice (Cooked)", "category": "grain", "calories": 216, "protein_g": 5, "carbs_g": 45, "fat_g": 1.8, "fiber_g": 3.5, "serving_size": "1 cup", "serving_weight_g": 195},
    {"name": "Chapati / Roti", "category": "grain", "calories": 104, "protein_g": 3.5, "carbs_g": 18, "fat_g": 2.5, "fiber_g": 2, "serving_size": "1 piece", "serving_weight_g": 40},
    {"name": "Naan Bread", "category": "grain", "calories": 262, "protein_g": 9, "carbs_g": 45, "fat_g": 5, "fiber_g": 2, "serving_size": "1 piece", "serving_weight_g": 90},
    {"name": "Paratha", "category": "grain", "calories": 260, "protein_g": 5, "carbs_g": 30, "fat_g": 13, "fiber_g": 2, "serving_size": "1 piece", "serving_weight_g": 80},
    {"name": "Dosa (Plain)", "category": "grain", "calories": 133, "protein_g": 3.9, "carbs_g": 19, "fat_g": 4.5, "fiber_g": 0.9, "serving_size": "1 piece", "serving_weight_g": 80},
    {"name": "Idli", "category": "grain", "calories": 58, "protein_g": 2, "carbs_g": 12, "fat_g": 0.4, "fiber_g": 0.6, "serving_size": "1 piece", "serving_weight_g": 40},
    {"name": "Upma", "category": "grain", "calories": 195, "protein_g": 5, "carbs_g": 28, "fat_g": 7, "fiber_g": 2, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Poha", "category": "grain", "calories": 180, "protein_g": 3, "carbs_g": 32, "fat_g": 5, "fiber_g": 1.5, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Puri", "category": "grain", "calories": 120, "protein_g": 2, "carbs_g": 12, "fat_g": 7, "fiber_g": 0.5, "serving_size": "1 piece", "serving_weight_g": 30},
    # ── Indian Curries & Dals ────────────────────────────────
    {"name": "Dal Tadka (Yellow Lentil)", "category": "legume", "calories": 150, "protein_g": 9, "carbs_g": 20, "fat_g": 4, "fiber_g": 5, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Rajma (Kidney Bean Curry)", "category": "legume", "calories": 180, "protein_g": 10, "carbs_g": 25, "fat_g": 5, "fiber_g": 7, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Chana Masala", "category": "legume", "calories": 210, "protein_g": 11, "carbs_g": 30, "fat_g": 6, "fiber_g": 8, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Paneer Butter Masala", "category": "dairy", "calories": 350, "protein_g": 18, "carbs_g": 12, "fat_g": 26, "fiber_g": 1, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Palak Paneer", "category": "dairy", "calories": 260, "protein_g": 16, "carbs_g": 10, "fat_g": 18, "fiber_g": 3, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Chicken Curry", "category": "meat", "calories": 250, "protein_g": 25, "carbs_g": 8, "fat_g": 14, "fiber_g": 1, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Butter Chicken", "category": "meat", "calories": 340, "protein_g": 28, "carbs_g": 10, "fat_g": 22, "fiber_g": 1, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Egg Curry", "category": "egg", "calories": 220, "protein_g": 14, "carbs_g": 8, "fat_g": 15, "fiber_g": 1, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Fish Curry", "category": "seafood", "calories": 200, "protein_g": 22, "carbs_g": 6, "fat_g": 10, "fiber_g": 1, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Aloo Gobi", "category": "vegetable", "calories": 150, "protein_g": 4, "carbs_g": 22, "fat_g": 6, "fiber_g": 4, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Baingan Bharta", "category": "vegetable", "calories": 140, "protein_g": 3, "carbs_g": 15, "fat_g": 8, "fiber_g": 4, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Sambar", "category": "legume", "calories": 130, "protein_g": 7, "carbs_g": 18, "fat_g": 4, "fiber_g": 5, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Rasam", "category": "soup", "calories": 50, "protein_g": 2, "carbs_g": 8, "fat_g": 1, "fiber_g": 1, "serving_size": "1 bowl", "serving_weight_g": 200},
    {"name": "Curd Rice", "category": "dairy", "calories": 200, "protein_g": 6, "carbs_g": 30, "fat_g": 6, "fiber_g": 1, "serving_size": "1 bowl", "serving_weight_g": 250},
    {"name": "Biryani (Chicken)", "category": "grain", "calories": 400, "protein_g": 22, "carbs_g": 50, "fat_g": 14, "fiber_g": 2, "serving_size": "1 plate", "serving_weight_g": 300},
    {"name": "Biryani (Veg)", "category": "grain", "calories": 320, "protein_g": 8, "carbs_g": 52, "fat_g": 10, "fiber_g": 3, "serving_size": "1 plate", "serving_weight_g": 300},
    # ── Proteins ─────────────────────────────────────────────
    {"name": "Grilled Chicken Breast", "category": "meat", "calories": 165, "protein_g": 31, "carbs_g": 0, "fat_g": 3.6, "fiber_g": 0, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Boiled Egg", "category": "egg", "calories": 78, "protein_g": 6.3, "carbs_g": 0.6, "fat_g": 5.3, "fiber_g": 0, "serving_size": "1 egg", "serving_weight_g": 50},
    {"name": "Egg White (Boiled)", "category": "egg", "calories": 17, "protein_g": 3.6, "carbs_g": 0.2, "fat_g": 0.1, "fiber_g": 0, "serving_size": "1 white", "serving_weight_g": 33},
    {"name": "Paneer (Cottage Cheese)", "category": "dairy", "calories": 265, "protein_g": 18, "carbs_g": 4, "fat_g": 20, "fiber_g": 0, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Tofu", "category": "soy", "calories": 76, "protein_g": 8, "carbs_g": 1.9, "fat_g": 4.8, "fiber_g": 0.3, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Chicken Tikka", "category": "meat", "calories": 190, "protein_g": 28, "carbs_g": 5, "fat_g": 7, "fiber_g": 0, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Fish (Rohu)", "category": "seafood", "calories": 97, "protein_g": 17, "carbs_g": 0, "fat_g": 3, "fiber_g": 0, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Prawns", "category": "seafood", "calories": 85, "protein_g": 18, "carbs_g": 0, "fat_g": 1.2, "fiber_g": 0, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Mutton (Goat)", "category": "meat", "calories": 143, "protein_g": 27, "carbs_g": 0, "fat_g": 3, "fiber_g": 0, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Whey Protein Shake", "category": "supplement", "calories": 120, "protein_g": 24, "carbs_g": 3, "fat_g": 1.5, "fiber_g": 0, "serving_size": "1 scoop", "serving_weight_g": 32},
    # ── Dairy ────────────────────────────────────────────────
    {"name": "Whole Milk", "category": "dairy", "calories": 149, "protein_g": 8, "carbs_g": 12, "fat_g": 8, "fiber_g": 0, "serving_size": "1 cup", "serving_weight_g": 244},
    {"name": "Curd / Yogurt", "category": "dairy", "calories": 61, "protein_g": 3.5, "carbs_g": 4.7, "fat_g": 3.3, "fiber_g": 0, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Greek Yogurt", "category": "dairy", "calories": 100, "protein_g": 17, "carbs_g": 6, "fat_g": 0.7, "fiber_g": 0, "serving_size": "1 cup", "serving_weight_g": 170},
    {"name": "Buttermilk / Chaas", "category": "dairy", "calories": 40, "protein_g": 3.3, "carbs_g": 5, "fat_g": 0.9, "fiber_g": 0, "serving_size": "1 glass", "serving_weight_g": 245},
    {"name": "Lassi (Sweet)", "category": "dairy", "calories": 170, "protein_g": 5, "carbs_g": 28, "fat_g": 5, "fiber_g": 0, "serving_size": "1 glass", "serving_weight_g": 250},
    # ── Fruits ───────────────────────────────────────────────
    {"name": "Banana", "category": "fruit", "calories": 89, "protein_g": 1.1, "carbs_g": 23, "fat_g": 0.3, "fiber_g": 2.6, "serving_size": "1 medium", "serving_weight_g": 118},
    {"name": "Apple", "category": "fruit", "calories": 52, "protein_g": 0.3, "carbs_g": 14, "fat_g": 0.2, "fiber_g": 2.4, "serving_size": "1 medium", "serving_weight_g": 182},
    {"name": "Mango", "category": "fruit", "calories": 60, "protein_g": 0.8, "carbs_g": 15, "fat_g": 0.4, "fiber_g": 1.6, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Papaya", "category": "fruit", "calories": 43, "protein_g": 0.5, "carbs_g": 11, "fat_g": 0.3, "fiber_g": 1.7, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Watermelon", "category": "fruit", "calories": 30, "protein_g": 0.6, "carbs_g": 7.6, "fat_g": 0.2, "fiber_g": 0.4, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Guava", "category": "fruit", "calories": 68, "protein_g": 2.6, "carbs_g": 14, "fat_g": 1, "fiber_g": 5.4, "serving_size": "1 medium", "serving_weight_g": 100},
    {"name": "Orange", "category": "fruit", "calories": 47, "protein_g": 0.9, "carbs_g": 12, "fat_g": 0.1, "fiber_g": 2.4, "serving_size": "1 medium", "serving_weight_g": 131},
    {"name": "Pomegranate", "category": "fruit", "calories": 83, "protein_g": 1.7, "carbs_g": 19, "fat_g": 1.2, "fiber_g": 4, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Grapes", "category": "fruit", "calories": 69, "protein_g": 0.7, "carbs_g": 18, "fat_g": 0.2, "fiber_g": 0.9, "serving_size": "100g", "serving_weight_g": 100},
    # ── Vegetables ───────────────────────────────────────────
    {"name": "Spinach (Palak)", "category": "vegetable", "calories": 23, "protein_g": 2.9, "carbs_g": 3.6, "fat_g": 0.4, "fiber_g": 2.2, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Broccoli", "category": "vegetable", "calories": 34, "protein_g": 2.8, "carbs_g": 7, "fat_g": 0.4, "fiber_g": 2.6, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Sweet Potato", "category": "vegetable", "calories": 86, "protein_g": 1.6, "carbs_g": 20, "fat_g": 0.1, "fiber_g": 3, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Potato (Boiled)", "category": "vegetable", "calories": 87, "protein_g": 1.9, "carbs_g": 20, "fat_g": 0.1, "fiber_g": 1.8, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Tomato", "category": "vegetable", "calories": 18, "protein_g": 0.9, "carbs_g": 3.9, "fat_g": 0.2, "fiber_g": 1.2, "serving_size": "1 medium", "serving_weight_g": 123},
    {"name": "Cucumber", "category": "vegetable", "calories": 16, "protein_g": 0.7, "carbs_g": 3.6, "fat_g": 0.1, "fiber_g": 0.5, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Onion", "category": "vegetable", "calories": 40, "protein_g": 1.1, "carbs_g": 9.3, "fat_g": 0.1, "fiber_g": 1.7, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Carrot", "category": "vegetable", "calories": 41, "protein_g": 0.9, "carbs_g": 10, "fat_g": 0.2, "fiber_g": 2.8, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Cauliflower", "category": "vegetable", "calories": 25, "protein_g": 1.9, "carbs_g": 5, "fat_g": 0.3, "fiber_g": 2, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Capsicum / Bell Pepper", "category": "vegetable", "calories": 31, "protein_g": 1, "carbs_g": 6, "fat_g": 0.3, "fiber_g": 2.1, "serving_size": "100g", "serving_weight_g": 100},
    # ── Nuts & Seeds ─────────────────────────────────────────
    {"name": "Almonds", "category": "nut", "calories": 579, "protein_g": 21, "carbs_g": 22, "fat_g": 50, "fiber_g": 12.5, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Peanuts", "category": "nut", "calories": 567, "protein_g": 26, "carbs_g": 16, "fat_g": 49, "fiber_g": 8.5, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Cashews", "category": "nut", "calories": 553, "protein_g": 18, "carbs_g": 30, "fat_g": 44, "fiber_g": 3.3, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Walnuts", "category": "nut", "calories": 654, "protein_g": 15, "carbs_g": 14, "fat_g": 65, "fiber_g": 6.7, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Peanut Butter", "category": "nut", "calories": 190, "protein_g": 8, "carbs_g": 6, "fat_g": 16, "fiber_g": 2, "serving_size": "2 tbsp", "serving_weight_g": 32},
    {"name": "Flax Seeds", "category": "seed", "calories": 534, "protein_g": 18, "carbs_g": 29, "fat_g": 42, "fiber_g": 27, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Chia Seeds", "category": "seed", "calories": 486, "protein_g": 17, "carbs_g": 42, "fat_g": 31, "fiber_g": 34, "serving_size": "100g", "serving_weight_g": 100},
    # ── Indian Snacks ────────────────────────────────────────
    {"name": "Samosa", "category": "snack", "calories": 260, "protein_g": 5, "carbs_g": 28, "fat_g": 14, "fiber_g": 2, "serving_size": "1 piece", "serving_weight_g": 100},
    {"name": "Vada Pav", "category": "snack", "calories": 290, "protein_g": 5, "carbs_g": 35, "fat_g": 14, "fiber_g": 2, "serving_size": "1 piece", "serving_weight_g": 120},
    {"name": "Pakora / Bhaji", "category": "snack", "calories": 180, "protein_g": 3, "carbs_g": 18, "fat_g": 11, "fiber_g": 1, "serving_size": "4 pieces", "serving_weight_g": 80},
    {"name": "Dhokla", "category": "snack", "calories": 130, "protein_g": 5, "carbs_g": 20, "fat_g": 3, "fiber_g": 1, "serving_size": "2 pieces", "serving_weight_g": 80},
    # ── International ────────────────────────────────────────
    {"name": "Oats (Cooked)", "category": "grain", "calories": 158, "protein_g": 6, "carbs_g": 27, "fat_g": 3.2, "fiber_g": 4, "serving_size": "1 cup", "serving_weight_g": 234},
    {"name": "Whole Wheat Bread", "category": "grain", "calories": 69, "protein_g": 3.6, "carbs_g": 12, "fat_g": 1.1, "fiber_g": 1.9, "serving_size": "1 slice", "serving_weight_g": 28},
    {"name": "Pasta (Cooked)", "category": "grain", "calories": 131, "protein_g": 5, "carbs_g": 25, "fat_g": 1.1, "fiber_g": 1.8, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Quinoa (Cooked)", "category": "grain", "calories": 120, "protein_g": 4.4, "carbs_g": 21, "fat_g": 1.9, "fiber_g": 2.8, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Avocado", "category": "fruit", "calories": 160, "protein_g": 2, "carbs_g": 9, "fat_g": 15, "fiber_g": 7, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Salmon", "category": "seafood", "calories": 208, "protein_g": 20, "carbs_g": 0, "fat_g": 13, "fiber_g": 0, "serving_size": "100g", "serving_weight_g": 100},
    {"name": "Tuna", "category": "seafood", "calories": 130, "protein_g": 29, "carbs_g": 0, "fat_g": 1, "fiber_g": 0, "serving_size": "100g", "serving_weight_g": 100},
    # ── Beverages ────────────────────────────────────────────
    {"name": "Green Tea", "category": "beverage", "calories": 2, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "fiber_g": 0, "serving_size": "1 cup", "serving_weight_g": 240},
    {"name": "Black Coffee", "category": "beverage", "calories": 2, "protein_g": 0.3, "carbs_g": 0, "fat_g": 0, "fiber_g": 0, "serving_size": "1 cup", "serving_weight_g": 240},
    {"name": "Masala Chai", "category": "beverage", "calories": 80, "protein_g": 2, "carbs_g": 12, "fat_g": 3, "fiber_g": 0, "serving_size": "1 cup", "serving_weight_g": 200},
    {"name": "Coconut Water", "category": "beverage", "calories": 46, "protein_g": 1.7, "carbs_g": 9, "fat_g": 0.5, "fiber_g": 2.6, "serving_size": "1 cup", "serving_weight_g": 240},
    # ── Sweets/Desserts ──────────────────────────────────────
    {"name": "Gulab Jamun", "category": "sweet", "calories": 150, "protein_g": 2, "carbs_g": 22, "fat_g": 6, "fiber_g": 0, "serving_size": "1 piece", "serving_weight_g": 45},
    {"name": "Rasgulla", "category": "sweet", "calories": 120, "protein_g": 3, "carbs_g": 22, "fat_g": 2, "fiber_g": 0, "serving_size": "1 piece", "serving_weight_g": 50},
    {"name": "Jalebi", "category": "sweet", "calories": 150, "protein_g": 1, "carbs_g": 30, "fat_g": 4, "fiber_g": 0, "serving_size": "1 piece", "serving_weight_g": 40},
    {"name": "Kheer", "category": "sweet", "calories": 180, "protein_g": 5, "carbs_g": 28, "fat_g": 6, "fiber_g": 0.5, "serving_size": "1 bowl", "serving_weight_g": 150},
    {"name": "Dark Chocolate", "category": "sweet", "calories": 170, "protein_g": 2, "carbs_g": 13, "fat_g": 12, "fiber_g": 3, "serving_size": "30g", "serving_weight_g": 30},
]

# ═══════════════════════════════════════════════════════════════
# EXERCISES — 55+
# ═══════════════════════════════════════════════════════════════

EXERCISES = [
    # ── Chest ────────────────────────────────────────────────
    {"name": "Flat Barbell Bench Press", "category": "strength", "difficulty": "intermediate", "equipment": "barbell, bench", "primary_muscle": "chest", "secondary_muscles": ["triceps", "shoulders"], "instructions": ["Lie flat on bench", "Grip barbell slightly wider than shoulder width", "Lower bar to mid-chest", "Press bar up to lockout"], "calories_per_minute": 8, "default_sets": 4, "default_reps": 8, "met_value": 6.0, "is_compound": True},
    {"name": "Incline Dumbbell Press", "category": "strength", "difficulty": "intermediate", "equipment": "dumbbell, bench", "primary_muscle": "upper chest", "secondary_muscles": ["shoulders", "triceps"], "instructions": ["Set bench to 30-45 degrees", "Press dumbbells up", "Lower with control"], "calories_per_minute": 7, "default_sets": 3, "default_reps": 10, "met_value": 5.5, "is_compound": True},
    {"name": "Push-Ups", "category": "strength", "difficulty": "beginner", "equipment": "bodyweight", "primary_muscle": "chest", "secondary_muscles": ["triceps", "shoulders", "core"], "instructions": ["Place hands shoulder-width apart", "Lower chest to ground", "Push back up", "Keep body straight"], "calories_per_minute": 7, "default_sets": 3, "default_reps": 15, "met_value": 3.8, "is_compound": True},
    {"name": "Cable Flyes", "category": "strength", "difficulty": "intermediate", "equipment": "cable machine", "primary_muscle": "chest", "instructions": ["Stand between cables", "Bring handles together in front", "Squeeze chest at peak"], "calories_per_minute": 5, "default_sets": 3, "default_reps": 12, "met_value": 4.0},
    # ── Back ─────────────────────────────────────────────────
    {"name": "Deadlift", "category": "strength", "difficulty": "advanced", "equipment": "barbell", "primary_muscle": "back", "secondary_muscles": ["glutes", "hamstrings", "core"], "instructions": ["Stand with feet hip-width", "Hinge at hips and grip bar", "Drive through heels to stand", "Keep back neutral"], "calories_per_minute": 10, "default_sets": 4, "default_reps": 5, "met_value": 6.0, "is_compound": True},
    {"name": "Pull-Ups", "category": "strength", "difficulty": "intermediate", "equipment": "pull-up bar", "primary_muscle": "lats", "secondary_muscles": ["biceps", "forearms"], "instructions": ["Grip bar overhand", "Pull chin above bar", "Lower with control"], "calories_per_minute": 8, "default_sets": 3, "default_reps": 8, "met_value": 8.0, "is_compound": True},
    {"name": "Barbell Rows", "category": "strength", "difficulty": "intermediate", "equipment": "barbell", "primary_muscle": "back", "secondary_muscles": ["biceps", "rear delts"], "instructions": ["Hinge forward 45 degrees", "Pull bar to lower chest", "Squeeze shoulder blades"], "calories_per_minute": 7, "default_sets": 4, "default_reps": 10, "met_value": 5.5, "is_compound": True},
    {"name": "Lat Pulldown", "category": "strength", "difficulty": "beginner", "equipment": "cable machine", "primary_muscle": "lats", "secondary_muscles": ["biceps"], "instructions": ["Grip bar wide", "Pull to upper chest", "Control the negative"], "calories_per_minute": 5, "default_sets": 3, "default_reps": 12, "met_value": 4.5},
    # ── Shoulders ────────────────────────────────────────────
    {"name": "Overhead Press", "category": "strength", "difficulty": "intermediate", "equipment": "barbell", "primary_muscle": "shoulders", "secondary_muscles": ["triceps", "core"], "instructions": ["Press barbell overhead", "Lock out arms", "Lower to shoulder level"], "calories_per_minute": 7, "default_sets": 4, "default_reps": 8, "met_value": 5.0, "is_compound": True},
    {"name": "Lateral Raises", "category": "strength", "difficulty": "beginner", "equipment": "dumbbell", "primary_muscle": "side delts", "instructions": ["Raise dumbbells to sides", "Stop at shoulder height", "Lower with control"], "calories_per_minute": 4, "default_sets": 3, "default_reps": 15, "met_value": 3.5},
    {"name": "Face Pulls", "category": "strength", "difficulty": "beginner", "equipment": "cable machine", "primary_muscle": "rear delts", "secondary_muscles": ["upper back"], "instructions": ["Pull rope to face", "Externally rotate at end", "Squeeze shoulder blades"], "calories_per_minute": 4, "default_sets": 3, "default_reps": 15, "met_value": 3.0},
    # ── Legs ─────────────────────────────────────────────────
    {"name": "Barbell Squat", "category": "strength", "difficulty": "intermediate", "equipment": "barbell, squat rack", "primary_muscle": "quadriceps", "secondary_muscles": ["glutes", "hamstrings", "core"], "instructions": ["Bar on upper back", "Squat to parallel or below", "Drive through heels"], "calories_per_minute": 9, "default_sets": 4, "default_reps": 8, "met_value": 6.0, "is_compound": True},
    {"name": "Leg Press", "category": "strength", "difficulty": "beginner", "equipment": "leg press machine", "primary_muscle": "quadriceps", "secondary_muscles": ["glutes"], "instructions": ["Place feet shoulder-width on platform", "Lower weight with control", "Press back up without locking knees"], "calories_per_minute": 6, "default_sets": 3, "default_reps": 12, "met_value": 5.0},
    {"name": "Romanian Deadlift", "category": "strength", "difficulty": "intermediate", "equipment": "barbell", "primary_muscle": "hamstrings", "secondary_muscles": ["glutes", "lower back"], "instructions": ["Hinge at hips", "Lower bar along legs", "Feel hamstring stretch", "Return to standing"], "calories_per_minute": 7, "default_sets": 3, "default_reps": 10, "met_value": 5.5, "is_compound": True},
    {"name": "Lunges", "category": "strength", "difficulty": "beginner", "equipment": "bodyweight", "primary_muscle": "quadriceps", "secondary_muscles": ["glutes", "hamstrings"], "instructions": ["Step forward", "Lower back knee to ground", "Push back to start"], "calories_per_minute": 6, "default_sets": 3, "default_reps": 12, "met_value": 4.0, "is_compound": True},
    {"name": "Leg Curls", "category": "strength", "difficulty": "beginner", "equipment": "machine", "primary_muscle": "hamstrings", "instructions": ["Curl weight toward glutes", "Squeeze at top", "Lower slowly"], "calories_per_minute": 4, "default_sets": 3, "default_reps": 12, "met_value": 3.5},
    {"name": "Calf Raises", "category": "strength", "difficulty": "beginner", "equipment": "bodyweight", "primary_muscle": "calves", "instructions": ["Rise onto toes", "Squeeze at top", "Lower slowly"], "calories_per_minute": 3, "default_sets": 4, "default_reps": 15, "met_value": 2.5},
    # ── Arms ─────────────────────────────────────────────────
    {"name": "Barbell Curl", "category": "strength", "difficulty": "beginner", "equipment": "barbell", "primary_muscle": "biceps", "instructions": ["Curl bar to shoulders", "Squeeze biceps", "Lower with control"], "calories_per_minute": 4, "default_sets": 3, "default_reps": 12, "met_value": 3.5},
    {"name": "Hammer Curls", "category": "strength", "difficulty": "beginner", "equipment": "dumbbell", "primary_muscle": "biceps", "secondary_muscles": ["forearms"], "instructions": ["Neutral grip curls", "Keep elbows stationary"], "calories_per_minute": 4, "default_sets": 3, "default_reps": 12, "met_value": 3.5},
    {"name": "Tricep Pushdown", "category": "strength", "difficulty": "beginner", "equipment": "cable machine", "primary_muscle": "triceps", "instructions": ["Push cable down", "Lock out elbows", "Control the return"], "calories_per_minute": 4, "default_sets": 3, "default_reps": 12, "met_value": 3.0},
    {"name": "Skull Crushers", "category": "strength", "difficulty": "intermediate", "equipment": "barbell, bench", "primary_muscle": "triceps", "instructions": ["Lower bar to forehead", "Extend arms to lockout", "Keep elbows in"], "calories_per_minute": 5, "default_sets": 3, "default_reps": 10, "met_value": 3.5},
    {"name": "Dips", "category": "strength", "difficulty": "intermediate", "equipment": "dip bars", "primary_muscle": "triceps", "secondary_muscles": ["chest", "shoulders"], "instructions": ["Lower body between bars", "Push back up", "Keep elbows close"], "calories_per_minute": 7, "default_sets": 3, "default_reps": 10, "met_value": 5.0, "is_compound": True},
    # ── Core ─────────────────────────────────────────────────
    {"name": "Plank", "category": "strength", "difficulty": "beginner", "equipment": "bodyweight", "primary_muscle": "core", "instructions": ["Hold push-up position on forearms", "Keep body straight", "Engage core throughout"], "calories_per_minute": 4, "default_sets": 3, "default_reps": 1, "default_rest_seconds": 30, "met_value": 3.8},
    {"name": "Crunches", "category": "strength", "difficulty": "beginner", "equipment": "bodyweight", "primary_muscle": "abs", "instructions": ["Lie on back", "Curl shoulders off floor", "Squeeze abs at top"], "calories_per_minute": 5, "default_sets": 3, "default_reps": 20, "met_value": 3.0},
    {"name": "Hanging Leg Raises", "category": "strength", "difficulty": "intermediate", "equipment": "pull-up bar", "primary_muscle": "abs", "secondary_muscles": ["hip flexors"], "instructions": ["Hang from bar", "Raise legs to 90 degrees", "Lower with control"], "calories_per_minute": 6, "default_sets": 3, "default_reps": 12, "met_value": 4.0},
    {"name": "Russian Twists", "category": "strength", "difficulty": "beginner", "equipment": "bodyweight", "primary_muscle": "obliques", "instructions": ["Sit with knees bent", "Rotate torso side to side", "Keep core engaged"], "calories_per_minute": 5, "default_sets": 3, "default_reps": 20, "met_value": 3.5},
    {"name": "Mountain Climbers", "category": "cardio", "difficulty": "beginner", "equipment": "bodyweight", "primary_muscle": "core", "secondary_muscles": ["shoulders", "quads"], "instructions": ["Start in push-up position", "Drive knees to chest alternately", "Maintain fast pace"], "calories_per_minute": 10, "default_sets": 3, "default_reps": 20, "met_value": 8.0, "is_compound": True},
    # ── Cardio ───────────────────────────────────────────────
    {"name": "Running (Outdoor)", "category": "cardio", "difficulty": "beginner", "equipment": "none", "primary_muscle": "full body", "instructions": ["Start with warm-up walk", "Maintain steady pace", "Cool down after"], "calories_per_minute": 11, "default_sets": 1, "default_reps": 1, "met_value": 9.8, "is_compound": True},
    {"name": "Jumping Jacks", "category": "cardio", "difficulty": "beginner", "equipment": "bodyweight", "primary_muscle": "full body", "instructions": ["Jump and spread arms/legs", "Return to start", "Maintain rhythm"], "calories_per_minute": 8, "default_sets": 3, "default_reps": 30, "met_value": 7.0, "is_compound": True},
    {"name": "Burpees", "category": "cardio", "difficulty": "intermediate", "equipment": "bodyweight", "primary_muscle": "full body", "instructions": ["Squat down", "Kick feet back to plank", "Do push-up", "Jump up explosively"], "calories_per_minute": 12, "default_sets": 3, "default_reps": 10, "met_value": 8.0, "is_compound": True},
    {"name": "Cycling", "category": "cardio", "difficulty": "beginner", "equipment": "bike", "primary_muscle": "quadriceps", "secondary_muscles": ["hamstrings", "calves"], "instructions": ["Maintain steady cadence", "Adjust resistance"], "calories_per_minute": 8, "default_sets": 1, "default_reps": 1, "met_value": 7.5},
    {"name": "Jump Rope", "category": "cardio", "difficulty": "beginner", "equipment": "jump rope", "primary_muscle": "full body", "instructions": ["Jump with both feet", "Keep wrists relaxed", "Maintain rhythm"], "calories_per_minute": 12, "default_sets": 3, "default_reps": 1, "met_value": 11.0, "is_compound": True},
    {"name": "Swimming", "category": "cardio", "difficulty": "intermediate", "equipment": "pool", "primary_muscle": "full body", "instructions": ["Choose stroke style", "Maintain breathing rhythm", "Use proper form"], "calories_per_minute": 10, "default_sets": 1, "default_reps": 1, "met_value": 8.0, "is_compound": True},
    # ── HIIT ─────────────────────────────────────────────────
    {"name": "Box Jumps", "category": "hiit", "difficulty": "intermediate", "equipment": "plyo box", "primary_muscle": "quadriceps", "secondary_muscles": ["glutes", "calves"], "instructions": ["Stand before box", "Jump onto box", "Step down carefully"], "calories_per_minute": 10, "default_sets": 3, "default_reps": 10, "met_value": 8.0, "is_compound": True},
    {"name": "Battle Ropes", "category": "hiit", "difficulty": "intermediate", "equipment": "battle ropes", "primary_muscle": "shoulders", "secondary_muscles": ["core", "arms"], "instructions": ["Create alternating waves", "Keep core tight", "Maintain intensity"], "calories_per_minute": 12, "default_sets": 3, "default_reps": 1, "met_value": 8.0},
    {"name": "Kettlebell Swings", "category": "hiit", "difficulty": "intermediate", "equipment": "kettlebell", "primary_muscle": "glutes", "secondary_muscles": ["hamstrings", "core", "shoulders"], "instructions": ["Hinge at hips", "Swing kettlebell to shoulder height", "Drive hips forward"], "calories_per_minute": 10, "default_sets": 3, "default_reps": 15, "met_value": 9.0, "is_compound": True},
    # ── Flexibility ──────────────────────────────────────────
    {"name": "Yoga Sun Salutation", "category": "flexibility", "difficulty": "beginner", "equipment": "yoga mat", "primary_muscle": "full body", "instructions": ["Flow through 12 poses", "Coordinate with breathing", "Hold each pose briefly"], "calories_per_minute": 4, "default_sets": 3, "default_reps": 1, "met_value": 3.0},
    {"name": "Static Stretching", "category": "flexibility", "difficulty": "beginner", "equipment": "none", "primary_muscle": "full body", "instructions": ["Hold each stretch 30 seconds", "Do not bounce", "Breathe deeply"], "calories_per_minute": 2, "default_sets": 1, "default_reps": 1, "met_value": 2.5},
]

# ═══════════════════════════════════════════════════════════════
# ACHIEVEMENTS
# ═══════════════════════════════════════════════════════════════

ACHIEVEMENTS = [
    {"name": "First Steps", "description": "Log your first step record", "category": "steps", "requirement_type": "count", "requirement_value": 1, "icon": "👣", "badge_color": "#10B981", "xp_reward": 50},
    {"name": "5K Walker", "description": "Walk 5,000 steps in a day", "category": "steps", "requirement_type": "count", "requirement_value": 5000, "icon": "🚶", "badge_color": "#3B82F6", "xp_reward": 100},
    {"name": "10K Champion", "description": "Walk 10,000 steps in a day", "category": "steps", "requirement_type": "count", "requirement_value": 10000, "icon": "🏆", "badge_color": "#F59E0B", "xp_reward": 200},
    {"name": "Marathon Walker", "description": "Walk 25,000 steps in a day", "category": "steps", "requirement_type": "count", "requirement_value": 25000, "icon": "🏅", "badge_color": "#EF4444", "xp_reward": 500},
    {"name": "First Workout", "description": "Complete your first workout", "category": "workout", "requirement_type": "count", "requirement_value": 1, "icon": "💪", "badge_color": "#8B5CF6", "xp_reward": 100},
    {"name": "Gym Rat", "description": "Complete 10 workouts", "category": "workout", "requirement_type": "total", "requirement_value": 10, "icon": "🏋️", "badge_color": "#EC4899", "xp_reward": 300},
    {"name": "Iron Will", "description": "Complete 50 workouts", "category": "workout", "requirement_type": "total", "requirement_value": 50, "icon": "⚡", "badge_color": "#F97316", "xp_reward": 1000},
    {"name": "Meal Logger", "description": "Log your first meal", "category": "nutrition", "requirement_type": "count", "requirement_value": 1, "icon": "🍽️", "badge_color": "#14B8A6", "xp_reward": 50},
    {"name": "Nutrition Master", "description": "Log 100 meals", "category": "nutrition", "requirement_type": "total", "requirement_value": 100, "icon": "🥗", "badge_color": "#22C55E", "xp_reward": 500},
    {"name": "Hydration Hero", "description": "Hit your water goal 7 days in a row", "category": "streak", "requirement_type": "streak", "requirement_value": 7, "icon": "💧", "badge_color": "#06B6D4", "xp_reward": 200},
    {"name": "Week Warrior", "description": "7-day step streak", "category": "streak", "requirement_type": "streak", "requirement_value": 7, "icon": "🔥", "badge_color": "#EF4444", "xp_reward": 300},
    {"name": "Month Master", "description": "30-day step streak", "category": "streak", "requirement_type": "streak", "requirement_value": 30, "icon": "🌟", "badge_color": "#F59E0B", "xp_reward": 1000},
]


async def seed_database():
    """Seed the database with sample data."""
    print("🌱 Starting database seed...")

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created")

    async with async_session_factory() as db:
        try:
            # ── 1. Seed Foods ────────────────────────────────────
            existing_food = await db.execute(text("SELECT COUNT(*) FROM foods"))
            if existing_food.scalar() == 0:
                for food_data in FOODS:
                    food = Food(**food_data, is_verified=True)
                    db.add(food)
                await db.flush()
                print(f"✅ Seeded {len(FOODS)} foods")
            else:
                print("⏭️  Foods already exist, skipping")

            # ── 2. Seed Exercises ────────────────────────────────
            existing_ex = await db.execute(text("SELECT COUNT(*) FROM exercises"))
            if existing_ex.scalar() == 0:
                for ex_data in EXERCISES:
                    exercise = Exercise(**ex_data)
                    db.add(exercise)
                await db.flush()
                print(f"✅ Seeded {len(EXERCISES)} exercises")
            else:
                print("⏭️  Exercises already exist, skipping")

            # ── 3. Seed Achievements ─────────────────────────────
            existing_ach = await db.execute(text("SELECT COUNT(*) FROM achievements"))
            if existing_ach.scalar() == 0:
                for ach_data in ACHIEVEMENTS:
                    ach = Achievement(**ach_data)
                    db.add(ach)
                await db.flush()
                print(f"✅ Seeded {len(ACHIEVEMENTS)} achievements")
            else:
                print("⏭️  Achievements already exist, skipping")

            # ── 4. Seed Demo Users ───────────────────────────────
            existing_users = await db.execute(text("SELECT COUNT(*) FROM users"))
            if existing_users.scalar() == 0:
                # Admin user
                admin = User(
                    email="admin@aifitness.com",
                    hashed_password=hash_password("Admin@1234"),
                    full_name="Admin User",
                    role="admin",
                    is_active=True,
                    is_verified=True,
                )
                db.add(admin)

                # Demo user
                demo = User(
                    email="demo@aifitness.com",
                    hashed_password=hash_password("Demo@1234"),
                    full_name="John Doe",
                    role="user",
                    is_active=True,
                    is_verified=True,
                )
                db.add(demo)
                await db.flush()

                # Demo user profile
                demo_profile = UserProfile(
                    user_id=demo.id,
                    date_of_birth=date(1995, 6, 15),
                    gender="male",
                    height_cm=175,
                    weight_kg=75.2,
                    target_weight_kg=72.0,
                    activity_level="moderate",
                    fitness_goal="lose_weight",
                    diet_preference="none",
                    daily_calorie_target=2200,
                    daily_protein_target=150,
                    daily_water_target_ml=3000,
                    daily_step_target=10000,
                )
                db.add(demo_profile)

                demo_settings = UserSettings(user_id=demo.id)
                db.add(demo_settings)

                admin_profile = UserProfile(user_id=admin.id, height_cm=170, weight_kg=68)
                db.add(admin_profile)
                await db.flush()

                print("✅ Seeded 2 users (admin + demo)")

                # ── 5. Seed 90 days of fitness history for demo user ─
                today = date.today()
                for days_ago in range(90):
                    d = today - timedelta(days=days_ago)

                    # Steps (varies 4000-14000)
                    steps = random.randint(4000, 14000)
                    step_record = StepsDaily(
                        user_id=demo.id,
                        date=d,
                        total_steps=steps,
                        distance_km=round(steps * 0.0007, 2),
                        calories_burned=round(steps * 0.04, 0),
                        walking_minutes=random.randint(20, 60),
                        goal_steps=10000,
                        goal_completed=steps >= 10000,
                        source="seed",
                    )
                    db.add(step_record)

                    # Water (1500-3500ml)
                    water_amount = random.randint(1500, 3500)
                    water_log = WaterLog(user_id=demo.id, date=d, amount_ml=water_amount)
                    db.add(water_log)

                    # BMI record every 7 days
                    if days_ago % 7 == 0:
                        weight = round(75.2 - (days_ago * 0.03) + random.uniform(-0.5, 0.5), 1)
                        bmi_val = round(weight / (1.75 ** 2), 1)
                        bmi_record = BMIRecord(
                            user_id=demo.id, date=d,
                            weight_kg=weight, height_cm=175,
                            bmi=bmi_val, category="normal" if bmi_val < 25 else "overweight",
                            bmr=round(10 * weight + 6.25 * 175 - 5 * 29 + 5),
                        )
                        db.add(bmi_record)

                    # Meals (2-3 per day, using random food IDs)
                    if days_ago < 30:  # Only last 30 days for meals
                        for meal_type in ["breakfast", "lunch", "dinner"]:
                            cal = random.randint(300, 800)
                            meal = Meal(
                                user_id=demo.id, date=d, meal_type=meal_type,
                                name=f"{meal_type.title()} meal",
                                total_calories=cal,
                                total_protein=round(cal * 0.25 / 4),
                                total_carbs=round(cal * 0.45 / 4),
                                total_fat=round(cal * 0.30 / 9),
                                total_fiber=round(random.uniform(2, 8), 1),
                            )
                            db.add(meal)

                    # Workout sessions (3-4 per week)
                    if random.random() < 0.5 and days_ago < 60:
                        workout = WorkoutSession(
                            user_id=demo.id, date=d,
                            name=random.choice(["Push Day", "Pull Day", "Leg Day", "Full Body", "Cardio"]),
                            workout_type=random.choice(["strength", "cardio", "hiit"]),
                            duration_minutes=random.randint(30, 75),
                            total_calories_burned=random.randint(200, 500),
                            total_volume_kg=random.randint(1000, 5000),
                            is_completed=True,
                        )
                        db.add(workout)

                await db.flush()
                print("✅ Seeded 90 days of fitness history")

                # ── 6. Notifications ─────────────────────────────
                for title, msg in [
                    ("Welcome! 🎉", "Welcome to AI Fitness Ecosystem! Set up your profile to get started."),
                    ("Step Goal Achieved! 🏆", "You hit 10,000 steps today!"),
                    ("Workout Reminder 💪", "Don't forget your Push Day workout today!"),
                    ("Weekly Report 📊", "Your weekly fitness report is ready."),
                ]:
                    notif = Notification(
                        user_id=demo.id, title=title, message=msg,
                        notification_type="system",
                    )
                    db.add(notif)
                await db.flush()
                print("✅ Seeded notifications")

            else:
                print("⏭️  Users already exist, skipping user data")

            await db.commit()
            print("\n🎉 Database seed complete!")
            print(f"   Foods: {len(FOODS)}")
            print(f"   Exercises: {len(EXERCISES)}")
            print(f"   Achievements: {len(ACHIEVEMENTS)}")
            print(f"   Users: 2 (admin + demo)")
            print(f"   Days of history: 90")

        except Exception as e:
            await db.rollback()
            print(f"\n❌ Seed failed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_database())
