"""
AI-related models: predictions and chat history.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON,
)
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class AIPrediction(TimestampMixin, Base):
    __tablename__ = "ai_predictions"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    prediction_type = Column(String(50), nullable=False)  # "weight", "calories", "performance"
    prediction_data = Column(JSON, nullable=False)  # Model output
    confidence = Column(Float, nullable=True)
    model_used = Column(String(100), nullable=True)
    input_data = Column(JSON, nullable=True)
    valid_until = Column(DateTime(timezone=True), nullable=True)


class AIChatHistory(TimestampMixin, Base):
    __tablename__ = "ai_chat_history"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    context_data = Column(JSON, nullable=True)  # Attached user fitness context

    user = relationship("User", back_populates="ai_chats")
