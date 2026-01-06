"""
Custom exceptions for the application.
"""


class FinAIException(Exception):
    """Base exception for FinAI application."""

    def __init__(self, message: str, code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AIServiceError(FinAIException):
    """Exception raised when AI service fails."""

    def __init__(self, message: str):
        super().__init__(message, code="AI_SERVICE_ERROR")


class SessionError(FinAIException):
    """Exception raised for session-related errors."""

    def __init__(self, message: str):
        super().__init__(message, code="SESSION_ERROR")


class ConfigurationError(FinAIException):
    """Exception raised for configuration errors."""

    def __init__(self, message: str):
        super().__init__(message, code="CONFIGURATION_ERROR")


class ValidationError(FinAIException):
    """Exception raised for validation errors."""

    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")
