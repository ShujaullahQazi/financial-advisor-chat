"""
Pydantic models for API request/response validation.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    history: List[str]
    session_id: Optional[str] = None
    user_preferences: Optional[Dict] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str
    session_id: str
    tools_used: List[str] = []
    confidence: float


class SessionData(BaseModel):
    """Model for session data storage."""

    user_id: str
    created_at: datetime
    preferences: Dict
    conversation_history: List[Dict]
    financial_profile: Dict
