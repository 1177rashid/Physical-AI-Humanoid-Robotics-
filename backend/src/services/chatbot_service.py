from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
import uuid
from datetime import datetime

from ..models.chat_session import ChatSession as ChatSessionModel, ChatMessage as ChatMessageModel
from ..models.user import User as UserModel
from .rag_service import rag_service
from ..utils.error_handler import CustomException, ErrorCode


class ChatbotService:
    @staticmethod
    def create_session(
        db: Session,
        session_title: str,
        user_id: Optional[UUID] = None
    ) -> ChatSessionModel:
        """Create a new chat session"""
        chat_session = ChatSessionModel(
            user_id=user_id,
            session_title=session_title,
            is_active=True
        )

        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

        return chat_session

    @staticmethod
    def get_session_by_id(db: Session, session_id: UUID) -> Optional[ChatSessionModel]:
        """Get a chat session by its ID"""
        query = select(ChatSessionModel).where(ChatSessionModel.id == session_id)
        return db.execute(query).scalar_one_or_none()

    @staticmethod
    def get_sessions_by_user(db: Session, user_id: UUID) -> List[ChatSessionModel]:
        """Get all chat sessions for a specific user"""
        query = select(ChatSessionModel).where(ChatSessionModel.user_id == user_id)
        return db.execute(query).scalars().all()

    @staticmethod
    def add_message_to_session(
        db: Session,
        session_id: UUID,
        role: str,
        content: str,
        context_sources: Optional[List[str]] = None,
        message_type: str = 'text'
    ) -> ChatMessageModel:
        """Add a message to a chat session"""
        if context_sources is None:
            context_sources = []

        message = ChatMessageModel(
            session_id=session_id,
            role=role,
            content=content,
            context_sources=context_sources,
            message_type=message_type
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    @staticmethod
    def get_messages_by_session(db: Session, session_id: UUID) -> List[ChatMessageModel]:
        """Get all messages in a chat session"""
        query = select(ChatMessageModel).where(
            ChatMessageModel.session_id == session_id
        ).order_by(ChatMessageModel.created_at.asc())
        return db.execute(query).scalars().all()

    @staticmethod
    def process_query_with_rag(query: str, session_id: Optional[UUID] = None) -> Dict[str, Any]:
        """Process a user query using RAG (Retrieval Augmented Generation)"""
        try:
            # Search for relevant content in the knowledge base
            search_results = rag_service.search_content(query, limit=5)

            # Prepare context from search results
            context_texts = [result['content'] for result in search_results]
            context_sources = [result['metadata'] for result in search_results]

            # For now, return a simple response with the context
            # In a real implementation, this would connect to an LLM
            response = f"I found information related to your query. Based on the textbook content, here's what I can tell you: {query[:100]}..."

            return {
                "response": response,
                "sources": context_sources,
                "timestamp": datetime.utcnow().isoformat(),
                "context_used": len(search_results) > 0
            }
        except Exception as e:
            raise CustomException(
                ErrorCode.INTERNAL_ERROR,
                detail=f"Error processing query with RAG: {str(e)}"
            )

    @staticmethod
    def process_voice_command(voice_input: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Process a voice command and convert it to an action"""
        try:
            # This would typically involve:
            # 1. Speech-to-text processing (if not already done)
            # 2. Natural language understanding
            # 3. Intent recognition
            # 4. Action mapping

            # For now, we'll simulate processing
            processed_input = voice_input.lower().strip()

            # Identify common robot commands
            if "move" in processed_input or "go" in processed_input:
                action_type = "navigation"
                # Extract direction and distance if present
                if "forward" in processed_input:
                    direction = "forward"
                elif "backward" in processed_input:
                    direction = "backward"
                elif "left" in processed_input:
                    direction = "left"
                elif "right" in processed_input:
                    direction = "right"
                else:
                    direction = "forward"

                # Extract distance if present
                distance = 1.0  # default 1 meter
                for word in processed_input.split():
                    if word.replace(".", "").isdigit():
                        try:
                            distance = float(word)
                            break
                        except ValueError:
                            continue

                action = {
                    "type": action_type,
                    "direction": direction,
                    "distance": distance,
                    "unit": "meters"
                }
            elif "pick" in processed_input or "grasp" in processed_input:
                action_type = "manipulation"
                action = {
                    "type": action_type,
                    "object": "unknown",  # Would extract from context
                    "action": "grasp"
                }
            elif "speak" in processed_input or "say" in processed_input:
                action_type = "communication"
                # Extract what should be said
                say_index = processed_input.find("say")
                if say_index == -1:
                    say_index = processed_input.find("speak")

                if say_index != -1:
                    response_text = processed_input[say_index + 3:].strip()
                    if response_text.startswith("to"):
                        response_text = response_text[2:].strip()
                else:
                    response_text = "Hello, I received a speech command"

                action = {
                    "type": action_type,
                    "text": response_text
                }
            else:
                # For other commands, treat as general query
                action_type = "query"
                action = {
                    "type": action_type,
                    "query": voice_input
                }

            return {
                "original_input": voice_input,
                "processed_action": action,
                "intent_confidence": 0.8,  # Simulated confidence
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise CustomException(
                ErrorCode.INTERNAL_ERROR,
                detail=f"Error processing voice command: {str(e)}"
            )

    @staticmethod
    def close_session(db: Session, session_id: UUID) -> bool:
        """Close a chat session"""
        session = ChatbotService.get_session_by_id(db, session_id)
        if not session:
            return False

        session.is_active = False
        db.commit()
        return True