"""
AI Fitness Coach chatbot service.
Provides context-aware fitness, nutrition, and workout advice.
"""

import json
import logging
import uuid
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

COACH_SYSTEM_PROMPT = """You are FitBot, an expert AI fitness coach. You have deep knowledge of:
- Exercise science, biomechanics, and workout programming
- Sports nutrition, macronutrients, micronutrients, and meal planning
- Weight management, body composition, and metabolic health
- Injury prevention, recovery, and mobility
- Mental fitness, motivation, and habit formation

User Context:
{user_context}

Rules:
1. Be encouraging, professional, and evidence-based
2. Personalize advice based on the user's profile, goals, and history
3. Provide specific, actionable recommendations
4. Use metric units unless the user prefers imperial
5. Include relevant numbers (calories, sets, reps, etc.)
6. Warn against unsafe practices
7. Keep responses concise but comprehensive (2-4 paragraphs)
8. Use emoji sparingly for friendliness 💪

If asked about medical conditions, recommend consulting a healthcare professional."""


class AICoachService:
    """Context-aware AI fitness coaching chatbot."""

    def __init__(self):
        self.provider = settings.AI_PROVIDER

    @property
    def is_available(self) -> bool:
        if self.provider == "openai":
            return bool(settings.OPENAI_API_KEY)
        return bool(settings.GEMINI_API_KEY)

    async def chat(
        self,
        message: str,
        user_context: dict,
        chat_history: list[dict] = None,
    ) -> dict:
        """Send a message to the AI coach and get a response."""
        if not self.is_available:
            return self._mock_response(message)

        try:
            context_str = json.dumps(user_context, indent=2, default=str)
            system_prompt = COACH_SYSTEM_PROMPT.format(user_context=context_str)

            if self.provider == "openai":
                return await self._chat_openai(message, system_prompt, chat_history or [])
            else:
                return await self._chat_gemini(message, system_prompt, chat_history or [])
        except Exception as e:
            logger.error(f"AI Coach error: {e}")
            return self._mock_response(message)

    async def _chat_openai(self, message: str, system_prompt: str, history: list) -> dict:
        import openai
        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        messages = [{"role": "system", "content": system_prompt}]
        for h in history[-10:]:  # Last 10 messages for context
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": message})

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
        )

        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens if response.usage else 0,
            "model": settings.OPENAI_MODEL,
        }

    async def _chat_gemini(self, message: str, system_prompt: str, history: list) -> dict:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            settings.GEMINI_MODEL,
            system_instruction=system_prompt,
        )

        chat = model.start_chat(
            history=[
                {"role": h["role"], "parts": [h["content"]]}
                for h in history[-10:]
            ]
        )
        response = await chat.send_message_async(message)

        return {
            "content": response.text,
            "tokens_used": 0,
            "model": settings.GEMINI_MODEL,
        }

    def _mock_response(self, message: str) -> dict:
        """Provide intelligent mock responses based on message keywords."""
        msg = message.lower()

        if any(w in msg for w in ["workout", "exercise", "training", "gym"]):
            content = (
                "💪 **Great question about training!**\n\n"
                "Based on your goals, I recommend a **Push/Pull/Legs split** — it's optimal for balanced development:\n\n"
                "- **Push Day**: Bench Press 4×8, OHP 3×10, Incline Dumbbell Press 3×12, Lateral Raises 3×15, Tricep Pushdowns 3×12\n"
                "- **Pull Day**: Deadlifts 4×6, Pull-ups 3×8, Barbell Rows 3×10, Face Pulls 3×15, Bicep Curls 3×12\n"
                "- **Legs Day**: Squats 4×8, Romanian Deadlifts 3×10, Leg Press 3×12, Leg Curls 3×12, Calf Raises 4×15\n\n"
                "Rest 60-90 seconds between sets. Progressive overload by adding 2.5kg weekly. "
                "Make sure you're eating enough protein (1.6-2.0g/kg body weight) to support muscle growth!"
            )
        elif any(w in msg for w in ["calorie", "diet", "nutrition", "eat", "food", "meal"]):
            content = (
                "🥗 **Nutrition is key to reaching your goals!**\n\n"
                "Here's a balanced approach:\n\n"
                "- **Protein**: Aim for 1.6-2.0g per kg of body weight (e.g., chicken, fish, eggs, legumes)\n"
                "- **Carbs**: Focus on complex carbs (oats, brown rice, sweet potatoes) — they fuel your workouts\n"
                "- **Fats**: Include healthy fats (avocado, nuts, olive oil) — 25-30% of total calories\n"
                "- **Fiber**: 25-30g daily from vegetables, fruits, and whole grains\n"
                "- **Hydration**: At least 2.5-3L of water daily\n\n"
                "**Meal Timing Tip**: Have protein within 2 hours post-workout for optimal recovery. "
                "A pre-workout meal 1-2 hours before training gives you sustained energy."
            )
        elif any(w in msg for w in ["weight", "lose", "fat", "slim", "lean"]):
            content = (
                "⚖️ **Weight management is about consistency!**\n\n"
                "The science is clear: a moderate calorie deficit of **300-500 calories/day** leads to sustainable fat loss "
                "(about 0.3-0.5kg per week).\n\n"
                "**Key strategies:**\n"
                "1. Track your calories — what gets measured gets managed\n"
                "2. Prioritize protein to preserve muscle mass during a deficit\n"
                "3. Combine resistance training with cardio (3:2 ratio)\n"
                "4. Get 7-9 hours of sleep — poor sleep increases hunger hormones\n"
                "5. Don't cut calories too aggressively — it backfires with metabolic adaptation\n\n"
                "Your TDEE calculator on the dashboard will help you find the right calorie target. "
                "Remember: progress > perfection! 🎯"
            )
        elif any(w in msg for w in ["motivat", "tired", "quit", "hard", "struggle"]):
            content = (
                "🔥 **I hear you, and I want you to know — every champion has days like this!**\n\n"
                "Here's what I'd suggest:\n\n"
                "1. **Remember your WHY** — revisit the goal that started your journey\n"
                "2. **Lower the bar** — on tough days, even a 15-minute walk counts\n"
                "3. **Track your wins** — look at your progress photos and stats\n"
                "4. **Change it up** — try a new workout, a new playlist, or train at a different time\n"
                "5. **Rest is productive** — sometimes the best thing is a recovery day\n\n"
                "You're already ahead of most people just by showing up and asking. "
                "Your streak data shows real commitment — don't discount that! Let's build on it together. 💪"
            )
        else:
            content = (
                "👋 **Hey there! I'm FitBot, your AI fitness coach!**\n\n"
                "I can help you with:\n\n"
                "- 🏋️ **Workout plans** — customized to your goals and experience level\n"
                "- 🥗 **Nutrition advice** — meal plans, macro calculations, food choices\n"
                "- ⚖️ **Weight management** — sustainable strategies for fat loss or muscle gain\n"
                "- 📊 **Progress analysis** — review your trends and get AI insights\n"
                "- 💡 **General fitness questions** — exercise form, recovery, supplements\n\n"
                "Just ask me anything! For the best personalized advice, make sure your profile is filled out "
                "with your current stats, goals, and activity level."
            )

        return {
            "content": content,
            "tokens_used": 0,
            "model": "mock",
        }


# Singleton
ai_coach_service = AICoachService()
