"""
AI Vision service for food detection and analysis.
Supports OpenAI GPT-4o Vision and Google Gemini Vision with graceful fallback to mock mode.
"""

import base64
import json
import logging
from typing import Optional

from app.core.config import settings
from app.schemas.nutrition import FoodScanResult, FoodScanResponse, FoodAnalysisResponse

logger = logging.getLogger(__name__)

# Structured prompt for consistent AI food analysis output
FOOD_SCAN_PROMPT = """Analyze this food image and identify ALL food items visible. For each item, provide:

Return a JSON array with objects containing these exact fields:
- food_name: string (specific food name)
- serving_size: string (e.g., "1 cup", "1 medium")
- estimated_weight_g: number
- confidence_score: number (0.0 to 1.0)
- calories: number (kcal)
- protein_g: number
- carbs_g: number
- fat_g: number
- fiber_g: number
- sugar_g: number
- sodium_mg: number
- calcium_mg: number
- iron_mg: number
- potassium_mg: number
- vitamin_a_mcg: number
- vitamin_c_mg: number
- vitamin_d_mcg: number
- magnesium_mg: number
- water_g: number
- bounding_box: object with x, y, w, h (normalized 0-1 coordinates) or null

Be as accurate as possible with nutrition data. Use USDA nutrition database values.
Return ONLY the JSON array, no other text."""

FOOD_ANALYSIS_PROMPT = """Analyze this food item in detail:
Food: {food_name}
Calories: {calories}
Protein: {protein_g}g, Carbs: {carbs_g}g, Fat: {fat_g}g

Provide a detailed analysis as JSON with these exact fields:
- healthy_rating: number (1-10, 10 being healthiest)
- processed_level: string ("none", "minimal", "moderate", "high", "ultra")
- diet_compatibility: object (keys: "keto", "vegan", "vegetarian", "paleo", "gluten_free", "dairy_free", values: boolean)
- weight_loss_score: number (1-10)
- muscle_gain_score: number (1-10)
- recommendation: string ("eat", "limit", "avoid")
- healthy_alternatives: array of strings (3-5 alternatives)
- best_time_to_eat: string (e.g., "Post-workout", "Breakfast")
- detailed_analysis: string (2-3 sentences about health impact)

Return ONLY the JSON object, no other text."""


class AIVisionService:
    """Handles food detection and analysis using AI vision models."""

    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self._openai_client = None
        self._gemini_model = None

    @property
    def is_available(self) -> bool:
        if self.provider == "openai":
            return bool(settings.OPENAI_API_KEY)
        return bool(settings.GEMINI_API_KEY)

    async def scan_food(self, image_data: bytes, mime_type: str = "image/jpeg") -> FoodScanResponse:
        """Scan food image and return detected items with nutrition data."""
        if not self.is_available:
            logger.info("AI Vision not configured, using mock data")
            return self._mock_scan_response()

        try:
            if self.provider == "openai":
                return await self._scan_with_openai(image_data, mime_type)
            else:
                return await self._scan_with_gemini(image_data, mime_type)
        except Exception as e:
            logger.error(f"AI Vision scan failed: {e}")
            return self._mock_scan_response()

    async def analyze_food(self, food_name: str, calories: float,
                           protein_g: float, carbs_g: float, fat_g: float) -> FoodAnalysisResponse:
        """Get detailed AI analysis of a food item."""
        if not self.is_available:
            return self._mock_analysis_response(food_name)

        try:
            prompt = FOOD_ANALYSIS_PROMPT.format(
                food_name=food_name, calories=calories,
                protein_g=protein_g, carbs_g=carbs_g, fat_g=fat_g,
            )

            if self.provider == "openai":
                result = await self._chat_openai(prompt)
            else:
                result = await self._chat_gemini(prompt)

            data = json.loads(result)
            return FoodAnalysisResponse(
                food_name=food_name,
                calories=calories,
                protein_g=protein_g,
                carbs_g=carbs_g,
                fat_g=fat_g,
                fiber_g=0,
                sugar_g=0,
                **data,
            )
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._mock_analysis_response(food_name)

    async def _scan_with_openai(self, image_data: bytes, mime_type: str) -> FoodScanResponse:
        """Use OpenAI GPT-4o Vision for food detection."""
        import openai

        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        b64_image = base64.b64encode(image_data).decode("utf-8")

        response = await client.chat.completions.create(
            model=settings.OPENAI_VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": FOOD_SCAN_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{b64_image}",
                                "detail": "high",
                            },
                        },
                    ],
                }
            ],
            max_tokens=2000,
            temperature=0.1,
        )

        result_text = response.choices[0].message.content.strip()
        # Clean potential markdown code blocks
        if result_text.startswith("```"):
            result_text = result_text.split("\n", 1)[1].rsplit("```", 1)[0]

        items_data = json.loads(result_text)
        items = [FoodScanResult(**item) for item in items_data]

        return FoodScanResponse(
            items=items,
            total_calories=sum(i.calories for i in items),
            total_protein=sum(i.protein_g for i in items),
            total_carbs=sum(i.carbs_g for i in items),
            total_fat=sum(i.fat_g for i in items),
        )

    async def _scan_with_gemini(self, image_data: bytes, mime_type: str) -> FoodScanResponse:
        """Use Google Gemini Vision for food detection."""
        import google.generativeai as genai

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)

        response = await model.generate_content_async(
            [
                FOOD_SCAN_PROMPT,
                {"mime_type": mime_type, "data": image_data},
            ],
            generation_config=genai.GenerationConfig(temperature=0.1, max_output_tokens=2000),
        )

        result_text = response.text.strip()
        if result_text.startswith("```"):
            result_text = result_text.split("\n", 1)[1].rsplit("```", 1)[0]

        items_data = json.loads(result_text)
        items = [FoodScanResult(**item) for item in items_data]

        return FoodScanResponse(
            items=items,
            total_calories=sum(i.calories for i in items),
            total_protein=sum(i.protein_g for i in items),
            total_carbs=sum(i.carbs_g for i in items),
            total_fat=sum(i.fat_g for i in items),
        )

    async def _chat_openai(self, prompt: str) -> str:
        import openai
        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()

    async def _chat_gemini(self, prompt: str) -> str:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        response = await model.generate_content_async(prompt)
        return response.text.strip()

    def _mock_scan_response(self) -> FoodScanResponse:
        """Return realistic mock data when AI is not configured."""
        items = [
            FoodScanResult(
                food_name="Grilled Chicken Breast",
                serving_size="1 piece (150g)",
                estimated_weight_g=150,
                confidence_score=0.94,
                calories=248,
                protein_g=46.5,
                carbs_g=0,
                fat_g=5.4,
                fiber_g=0,
                sugar_g=0,
                sodium_mg=104,
                calcium_mg=18,
                iron_mg=1.5,
                potassium_mg=358,
                vitamin_a_mcg=9,
                vitamin_c_mg=0,
                vitamin_d_mcg=0.2,
                magnesium_mg=37,
                water_g=95,
                bounding_box={"x": 0.1, "y": 0.2, "w": 0.4, "h": 0.3},
            ),
            FoodScanResult(
                food_name="Steamed Brown Rice",
                serving_size="1 cup (195g)",
                estimated_weight_g=195,
                confidence_score=0.91,
                calories=216,
                protein_g=5.0,
                carbs_g=44.8,
                fat_g=1.8,
                fiber_g=3.5,
                sugar_g=0.7,
                sodium_mg=10,
                calcium_mg=20,
                iron_mg=0.8,
                potassium_mg=154,
                vitamin_a_mcg=0,
                vitamin_c_mg=0,
                vitamin_d_mcg=0,
                magnesium_mg=84,
                water_g=143,
                bounding_box={"x": 0.5, "y": 0.3, "w": 0.35, "h": 0.25},
            ),
            FoodScanResult(
                food_name="Mixed Green Salad",
                serving_size="1 bowl (100g)",
                estimated_weight_g=100,
                confidence_score=0.88,
                calories=20,
                protein_g=1.8,
                carbs_g=3.3,
                fat_g=0.2,
                fiber_g=2.0,
                sugar_g=1.3,
                sodium_mg=27,
                calcium_mg=72,
                iron_mg=1.5,
                potassium_mg=312,
                vitamin_a_mcg=375,
                vitamin_c_mg=28,
                vitamin_d_mcg=0,
                magnesium_mg=14,
                water_g=94,
                bounding_box={"x": 0.15, "y": 0.55, "w": 0.3, "h": 0.25},
            ),
        ]

        return FoodScanResponse(
            items=items,
            total_calories=sum(i.calories for i in items),
            total_protein=sum(i.protein_g for i in items),
            total_carbs=sum(i.carbs_g for i in items),
            total_fat=sum(i.fat_g for i in items),
        )

    def _mock_analysis_response(self, food_name: str) -> FoodAnalysisResponse:
        return FoodAnalysisResponse(
            food_name=food_name,
            calories=250,
            protein_g=30,
            carbs_g=15,
            fat_g=8,
            fiber_g=3,
            sugar_g=2,
            healthy_rating=7.5,
            processed_level="minimal",
            diet_compatibility={
                "keto": False, "vegan": False, "vegetarian": False,
                "paleo": True, "gluten_free": True, "dairy_free": True,
            },
            weight_loss_score=7,
            muscle_gain_score=9,
            recommendation="eat",
            healthy_alternatives=[
                "Turkey breast", "Tofu stir-fry", "Salmon fillet",
                "Lentil soup", "Egg white omelette",
            ],
            best_time_to_eat="Post-workout or lunch",
            detailed_analysis=(
                f"{food_name} is an excellent source of lean protein, ideal for muscle recovery. "
                "Low in saturated fat and rich in essential amino acids. "
                "Pair with complex carbs and vegetables for a balanced meal."
            ),
        )


# Singleton instance
ai_vision_service = AIVisionService()
