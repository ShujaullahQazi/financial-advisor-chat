"""
FastAPI routes for the financial advisor chat application.
"""

import json
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from ..agent import FinancialAgent
from ..services.genai_service import GenAIService
from ..services.session_service import SessionService
from ..utils.logger import logger
from .models import ChatRequest, ChatResponse

router = APIRouter()

# Initialize services
session_service = SessionService()
genai_service = GenAIService()
agent = FinancialAgent()


@router.get("/")
async def root():
    """Serve the main chat interface."""
    return FileResponse("static/index.html")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return AI response.

    Args:
        request: Chat request with history and optional session info

    Returns:
        ChatResponse with AI response, session ID, tools used, and confidence
    """
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        session_data = session_service.get_or_create_session(
            session_id=session_id, preferences=request.user_preferences
        )

        # Get the latest user message
        latest_message = request.history[-1] if request.history else ""

        # Check for calculation requests
        calculation_request = agent.detect_calculation_request(latest_message)
        tools_used = []
        calculation_result = None

        if calculation_request:
            numbers = agent.extract_numbers(latest_message)
            if numbers:
                calculation_result = agent.execute_tool(calculation_request["tool"], numbers)
                tools_used.append(calculation_request["description"])

        # Build enhanced prompt
        context = agent.get_enhanced_context(session_data)

        # Add calculation results to context if available
        if calculation_result and "error" not in calculation_result:
            context += f"\n\nCALCULATION RESULT:\n{json.dumps(calculation_result, indent=2)}\n\nPlease explain these results to the user in a clear, educational manner."

        # Combine context with conversation history
        full_prompt = context + "\n\nCONVERSATION HISTORY:\n" + "\n".join(request.history)

        # Generate response
        response_text = await genai_service.generate_response(full_prompt)

        # Update session
        session_service.add_conversation_entry(
            session_id=session_id,
            user_message=latest_message,
            ai_response=response_text,
            tools_used=tools_used,
        )

        # Calculate confidence
        confidence = 0.9 if calculation_result else 0.8

        logger.info(f"Chat processed for session {session_id}, tools: {tools_used}")

        return ChatResponse(
            response=response_text,
            session_id=session_id,
            tools_used=tools_used,
            confidence=confidence,
        )

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session information."""
    session = session_service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    session_service.delete_session(session_id)
    return {"message": "Session deleted"}
