"""
Session management service.
Handles session CRUD operations with in-memory storage.
Can be extended to use database storage in production.
"""

from datetime import datetime
from typing import Dict, List, Optional

from ..utils.logger import logger


class SessionService:
    """
    Service for managing user sessions.

    Uses in-memory storage by default. For production,
    extend this class to use Redis, PostgreSQL, or other storage.
    """

    def __init__(self):
        """Initialize session service with in-memory storage."""
        self._sessions: Dict[str, Dict] = {}

    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get session by ID.

        Args:
            session_id: Session identifier

        Returns:
            Session data dictionary or None if not found
        """
        return self._sessions.get(session_id)

    def get_or_create_session(self, session_id: str, preferences: Optional[Dict] = None) -> Dict:
        """
        Get existing session or create a new one.

        Args:
            session_id: Session identifier
            preferences: Optional user preferences

        Returns:
            Session data dictionary
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "session_id": session_id,
                "created_at": datetime.now(),
                "conversation_history": [],
                "preferences": preferences or {},
                "financial_profile": {},
            }
            logger.info(f"Created new session: {session_id}")

        return self._sessions[session_id]

    def add_conversation_entry(
        self, session_id: str, user_message: str, ai_response: str, tools_used: List[str]
    ) -> None:
        """
        Add a conversation entry to session history.

        Args:
            session_id: Session identifier
            user_message: User's message
            ai_response: AI's response
            tools_used: List of tools used in response
        """
        if session_id in self._sessions:
            self._sessions[session_id]["conversation_history"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "user_message": user_message,
                    "ai_response": ai_response,
                    "tools_used": tools_used,
                }
            )

    def update_preferences(self, session_id: str, preferences: Dict) -> None:
        """
        Update session preferences.

        Args:
            session_id: Session identifier
            preferences: New preferences to merge
        """
        if session_id in self._sessions:
            self._sessions[session_id]["preferences"].update(preferences)

    def update_financial_profile(self, session_id: str, profile: Dict) -> None:
        """
        Update session financial profile.

        Args:
            session_id: Session identifier
            profile: New profile data to merge
        """
        if session_id in self._sessions:
            self._sessions[session_id]["financial_profile"].update(profile)

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: Session identifier

        Returns:
            True if session was deleted, False if not found
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False

    def get_all_sessions(self) -> Dict[str, Dict]:
        """
        Get all sessions (admin use).

        Returns:
            Dictionary of all sessions
        """
        return self._sessions.copy()
