"""
Application settings using pydantic-settings for environment management.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    google_api_key: str = Field(..., description="Google Gemini API key")

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")

    # Environment
    environment: str = Field(
        default="development", description="Environment (development, staging, production)"
    )
    debug: bool = Field(default=False, description="Debug mode")

    # CORS
    cors_origins: list[str] = Field(default=["*"], description="Allowed CORS origins")

    # Session Configuration
    session_timeout_hours: int = Field(default=24, description="Session timeout in hours")
    max_history_length: int = Field(default=50, description="Maximum conversation history length")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
