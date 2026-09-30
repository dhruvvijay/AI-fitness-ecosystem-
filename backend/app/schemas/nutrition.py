"""
Pydantic schemas for nutrition, meals, and food scanning.
"""

from datetime import date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ── Food ─────────────────────────────────────────────────────────

class FoodResponse(BaseModel):
    id: int
    name: str
    category: Optional[str]
    serving_size: Optional[str]
    serving_weight_g: Optional[float]
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    sugar_g: float
    sodium_mg: float
    calcium_mg: float
    iron_mg: float
    potassium_mg: float
    vitamin_a_mcg: float
    vitamin_c_mg: float
    vitamin_d_mcg: float
    magnesium_mg: float
    water_g: float
    image_url: Optional[str]
    is_verified: bool
    model_config = {"from_attributes": True}

class FoodSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class CreateFoodRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = None
    serving_size: Optional[str] = None
    serving_weight_g: Optional[float] = Field(None, ge=0)
    calories: float = Field(..., ge=0)
    protein_g: float = Field(default=0, ge=0)
    carbs_g: float = Field(default=0, ge=0)
    fat_g: float = Field(default=0, ge=0)
    fiber_g: float = Field(default=0, ge=0)
    sugar_g: float = Field(default=0, ge=0)
    sodium_mg: float = Field(default=0, ge=0)


# ── AI Food Scan ─────────────────────────────────────────────────

class FoodScanResult(BaseModel):
    food_name: str
    serving_size: str
    estimated_weight_g: float
    confidence_score: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    sugar_g: float
    sodium_mg: float
    calcium_mg: float
    iron_mg: float
    potassium_mg: float
    vitamin_a_mcg: float
    vitamin_c_mg: float
    vitamin_d_mcg: float
    magnesium_mg: float
    water_g: float
    bounding_box: Optional[Dict[str, float]] = None  # {"x": 0.1, "y": 0.2, "w": 0.3, "h": 0.4}

class FoodScanResponse(BaseModel):
    items: List[FoodScanResult]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    image_url: Optional[str] = None


class FoodAnalysisResponse(BaseModel):
    food_name: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    sugar_g: float
    healthy_rating: float  # 1-10
    processed_level: str
    diet_compatibility: Dict[str, bool]
    weight_loss_score: float
    muscle_gain_score: float
    recommendation: str  # "eat", "limit", "avoid"
    healthy_alternatives: List[str]
    best_time_to_eat: str
    detailed_analysis: str


# ── Meals ────────────────────────────────────────────────────────

class MealItemRequest(BaseModel):
    food_id: int
    servings: float = Field(default=1.0, ge=0.1, le=100)
    custom_weight_g: Optional[float] = Field(None, ge=0)

class CreateMealRequest(BaseModel):
    date: date
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    name: Optional[str] = None
    items: List[MealItemRequest]
    notes: Optional[str] = None

class MealItemResponse(BaseModel):
    id: int
    food_id: int
    food_name: str
    servings: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    model_config = {"from_attributes": True}

class MealResponse(BaseModel):
    id: int
    date: date
    meal_type: str
    name: Optional[str]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    total_fiber: float
    items: List[MealItemResponse]
    is_ai_generated: bool
    model_config = {"from_attributes": True}


# ── Meal Plan ────────────────────────────────────────────────────

class MealPlanRequest(BaseModel):
    target_calories: int = Field(..., ge=800, le=10000)
    diet_preference: str = "none"
    fitness_goal: str = "maintain"
    meals_per_day: int = Field(default=4, ge=2, le=6)
    exclude_foods: Optional[List[str]] = None

class MealPlanMeal(BaseModel):
    meal_type: str
    name: str
    foods: List[Dict[str, Any]]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    recipe: Optional[str] = None

class MealPlanResponse(BaseModel):
    target_calories: int
    actual_calories: float
    meals: List[MealPlanMeal]
    total_protein: float
    total_carbs: float
    total_fat: float
    total_fiber: float
    notes: str
