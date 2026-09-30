"""
Nutrition models: foods, food images, nutrition data, meals, meal items.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, DateTime, Text,
    ForeignKey, JSON, Enum as SAEnum,
)
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class Food(TimestampMixin, Base):
    __tablename__ = "foods"

    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=True)  # "fruit", "vegetable", "grain", "protein", etc.
    serving_size = Column(String(100), nullable=True)
    serving_weight_g = Column(Float, nullable=True)
    calories = Column(Float, nullable=False)
    protein_g = Column(Float, default=0.0)
    carbs_g = Column(Float, default=0.0)
    fat_g = Column(Float, default=0.0)
    fiber_g = Column(Float, default=0.0)
    sugar_g = Column(Float, default=0.0)
    sodium_mg = Column(Float, default=0.0)
    calcium_mg = Column(Float, default=0.0)
    iron_mg = Column(Float, default=0.0)
    potassium_mg = Column(Float, default=0.0)
    vitamin_a_mcg = Column(Float, default=0.0)
    vitamin_c_mg = Column(Float, default=0.0)
    vitamin_d_mcg = Column(Float, default=0.0)
    magnesium_mg = Column(Float, default=0.0)
    water_g = Column(Float, default=0.0)
    is_verified = Column(Boolean, default=False)
    barcode = Column(String(50), nullable=True, index=True)
    brand = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=True)
    is_custom = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    images = relationship("FoodImage", back_populates="food", cascade="all, delete-orphan")
    meal_items = relationship("MealItem", back_populates="food")


class FoodImage(TimestampMixin, Base):
    __tablename__ = "food_images"

    food_id = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    confidence_score = Column(Float, nullable=True)
    detected_items = Column(JSON, nullable=True)  # Store bounding box data
    ai_provider = Column(String(50), nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    food = relationship("Food", back_populates="images")


class NutritionData(TimestampMixin, Base):
    """Extended nutrition analysis data from AI scanning."""
    __tablename__ = "nutrition_data"

    food_id = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"), nullable=False, index=True)
    healthy_rating = Column(Float, nullable=True)  # 1-10
    processed_level = Column(String(20), nullable=True)  # "none", "minimal", "moderate", "high", "ultra"
    diet_compatibility = Column(JSON, nullable=True)  # {"keto": true, "vegan": false, ...}
    weight_loss_score = Column(Float, nullable=True)  # 1-10
    muscle_gain_score = Column(Float, nullable=True)  # 1-10
    recommendation = Column(String(20), nullable=True)  # "eat", "limit", "avoid"
    healthy_alternatives = Column(JSON, nullable=True)
    best_time_to_eat = Column(String(100), nullable=True)
    ai_analysis = Column(Text, nullable=True)


class Meal(TimestampMixin, Base):
    __tablename__ = "meals"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    meal_type = Column(
        SAEnum("breakfast", "lunch", "dinner", "snack", name="meal_type"),
        nullable=False,
    )
    name = Column(String(255), nullable=True)
    total_calories = Column(Float, default=0.0)
    total_protein = Column(Float, default=0.0)
    total_carbs = Column(Float, default=0.0)
    total_fat = Column(Float, default=0.0)
    total_fiber = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_ai_generated = Column(Boolean, default=False)

    user = relationship("User", back_populates="meals")
    items = relationship("MealItem", back_populates="meal", cascade="all, delete-orphan")


class MealItem(TimestampMixin, Base):
    __tablename__ = "meal_items"

    meal_id = Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), nullable=False, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False, index=True)
    servings = Column(Float, default=1.0, nullable=False)
    custom_weight_g = Column(Float, nullable=True)
    calories = Column(Float, nullable=False)
    protein_g = Column(Float, default=0.0)
    carbs_g = Column(Float, default=0.0)
    fat_g = Column(Float, default=0.0)

    meal = relationship("Meal", back_populates="items")
    food = relationship("Food", back_populates="meal_items")
