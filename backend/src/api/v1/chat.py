from fastapi import APIRouter, HTTPException, Depends, WebSocket
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime

from pydantic import BaseModel
from ...services.chatbot_service import ChatbotService
from ...config.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


# Pydantic models for API responses
class ChatSession(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    session_title: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    context_sources: List[str]
    message_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[UUID] = None
    context: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    sources: List[dict]
    timestamp: str
    context_used: bool


class ChatSessionRequest(BaseModel):
    initial_query: Optional[str] = None


class VoiceCommandRequest(BaseModel):
    session_id: UUID
    voice_input: str
    context: Optional[str] = None


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db=Depends(get_db)):
    """
    Chat endpoint that processes user messages and returns bot responses
    """
    try:
        # If no session ID is provided, create a new session
        if not request.session_id:
            session_title = request.message[:50] + "..." if len(request.message) > 50 else request.message
            session = ChatbotService.create_session(db, session_title)
            session_id = session.id
        else:
            # Validate that the session exists
            session = ChatbotService.get_session_by_id(db, request.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            session_id = request.session_id

        # Add user message to session
        user_message = ChatbotService.add_message_to_session(
            db, session_id, "user", request.message, message_type="text"
        )

        # Process the query using RAG
        response_data = ChatbotService.process_query_with_rag(request.message, session_id)

        # Add bot response to session
        bot_message = ChatbotService.add_message_to_session(
            db, session_id, "assistant", response_data["response"],
            context_sources=response_data.get("sources", []),
            message_type="text"
        )

        return ChatResponse(
            response=response_data["response"],
            sources=response_data.get("sources", []),
            timestamp=response_data["timestamp"],
            context_used=response_data["context_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.post("/session", response_model=ChatSession)
async def create_chat_session(request: ChatSessionRequest, db=Depends(get_db)):
    """
    Create a new chat session
    """
    try:
        session_title = request.initial_query[:50] + "..." if request.initial_query else "New Chat Session"
        session = ChatbotService.create_session(db, session_title)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat session: {str(e)}")


@router.get("/session/{session_id}", response_model=ChatSession)
async def get_chat_session(session_id: UUID, db=Depends(get_db)):
    """
    Get a specific chat session
    """
    try:
        session = ChatbotService.get_session_by_id(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving session: {str(e)}")


@router.get("/session/{session_id}/messages", response_model=List[ChatMessage])
async def get_chat_messages(session_id: UUID, db=Depends(get_db)):
    """
    Get all messages in a specific chat session
    """
    try:
        # Verify session exists
        session = ChatbotService.get_session_by_id(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        messages = ChatbotService.get_messages_by_session(db, session_id)
        return messages
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")


@router.post("/voice-command", response_model=dict)
async def process_voice_command(request: VoiceCommandRequest, db=Depends(get_db)):
    """
    Process a voice command and convert it to an action
    """
    try:
        # Verify session exists
        session = ChatbotService.get_session_by_id(db, request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Process the voice command
        result = ChatbotService.process_voice_command(request.voice_input, request.context)

        # Add user voice command to session
        ChatbotService.add_message_to_session(
            db, request.session_id, "user", request.voice_input,
            message_type="voice"
        )

        # Add the processed action to session
        action_response = f"Processed voice command: {request.voice_input}. Action: {result['processed_action']['type']}"
        ChatbotService.add_message_to_session(
            db, request.session_id, "assistant", action_response,
            message_type="action"
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice command: {str(e)}")


@router.post("/session/{session_id}/close")
async def close_chat_session(session_id: UUID, db=Depends(get_db)):
    """
    Close a chat session
    """
    try:
        success = ChatbotService.close_session(db, session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session closed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error closing session: {str(e)}")