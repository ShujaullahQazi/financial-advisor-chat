"""
FinAI - Financial Advisor AI Agent
Root entry point for running the application.

Usage:
    python run_app.py
"""

import uvicorn

from src.config.settings import settings


def main():
    """Run the FinAI application."""
    uvicorn.run(
        "src.main:app", host=settings.host, port=settings.port, reload=not settings.is_production
    )


if __name__ == "__main__":
    main()
