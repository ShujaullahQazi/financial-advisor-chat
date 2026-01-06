"""
FinAI - Financial Advisor AI Agent
Main application entry point.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api.routes import router
from .config.settings import settings
from .utils.logger import logger

# Create FastAPI app
app = FastAPI(
    title="FinAI - Financial Advisor",
    description="AI-powered financial advisor agent built with FastAPI and Google Gemini",
    version="2.0.0",
)

# Include API routes
app.include_router(router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    """Application startup handler."""
    logger.info(f"Starting FinAI in {settings.environment} mode")
    logger.info(f"Server running on {settings.host}:{settings.port}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown handler."""
    logger.info("Shutting down FinAI")


def run():
    """Run the application with uvicorn."""
    uvicorn.run(
        "src.main:app", host=settings.host, port=settings.port, reload=not settings.is_production
    )


if __name__ == "__main__":
    run()
