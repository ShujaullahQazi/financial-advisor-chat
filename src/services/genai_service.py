"""
Google Gemini AI service wrapper.
Handles AI model initialization and response generation.
"""

import google.generativeai as genai

from ..config import API_CONFIG
from ..config.settings import settings
from ..utils.exceptions import AIServiceError
from ..utils.logger import logger


class GenAIService:
    """
    Service wrapper for Google Gemini AI.

    Provides a clean interface for AI interactions with
    error handling and logging.
    """

    def __init__(self):
        """Initialize the Gemini AI service."""
        self._configure_api()
        self._model = genai.GenerativeModel(API_CONFIG["model"])
        logger.info(f"GenAI service initialized with model: {API_CONFIG['model']}")

    def _configure_api(self) -> None:
        """Configure the Gemini API with credentials."""
        try:
            genai.configure(api_key=settings.google_api_key)
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {str(e)}")
            raise AIServiceError("Failed to initialize AI service. Check API key configuration.")

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the AI model.

        Args:
            prompt: The prompt to send to the model

        Returns:
            Generated response text

        Raises:
            AIServiceError: If response generation fails
        """
        try:
            response = self._model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"AI generation error: {str(e)}")
            raise AIServiceError(f"Failed to generate response: {str(e)}")

    def generate_response_sync(self, prompt: str) -> str:
        """
        Synchronous version of response generation.

        Args:
            prompt: The prompt to send to the model

        Returns:
            Generated response text
        """
        try:
            response = self._model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"AI generation error: {str(e)}")
            raise AIServiceError(f"Failed to generate response: {str(e)}")

    @property
    def model_name(self) -> str:
        """Get the current model name."""
        return API_CONFIG["model"]
