"""
WebSocket handler for real-time chat.
"""

import json

from fastapi import WebSocket, WebSocketDisconnect

from ..utils.logger import logger


async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time chat communication.

    Args:
        websocket: WebSocket connection
        session_id: Session identifier
    """
    await websocket.accept()
    logger.info(f"WebSocket connected for session {session_id}")

    try:
        while True:
            data = await websocket.receive_text()
            json.loads(data)

            # TODO: Process message similar to HTTP endpoint
            # For now, send acknowledgment
            response = {
                "type": "message",
                "content": "WebSocket response",
                "session_id": session_id,
            }
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {str(e)}")
