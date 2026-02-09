from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime

from src.middleware.auth import jwt_scheme, get_current_user_id
from src.core.database import get_session
from src.core.logging import log_chat_interaction, log_api_call, log_error
from src.core.errors import ConversationNotFoundError

# Create the chat router
router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list = []


@router.post("/{user_id}")
async def chat(
    user_id: str,
    request: ChatRequest,
    token: str = Depends(jwt_scheme),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Chat endpoint that processes user messages and returns AI responses
    """
    start_time = datetime.now()

    try:
        # Get the current user ID from the request
        current_user_id = get_current_user_id(request=request)

        # Verify that the user_id in the path matches the authenticated user
        if current_user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID in path does not match authenticated user"
            )

        # Lazy load services inside the function
        from src.services.conversation_service import ConversationService, MessageService

        # Import and initialize agent service inside the function
        from src.services.agent_service import AgentService
        agent_service = AgentService()

        conversation_service = ConversationService()
        message_service = MessageService()

        # Get or create conversation
        if request.conversation_id:
            conversation = conversation_service.get_conversation_by_id(session, request.conversation_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation with id {request.conversation_id} not found"
                )
        else:
            # Create a new conversation
            conversation = conversation_service.create_conversation(session, user_id)

        # Save the user's message to the database
        user_message = message_service.create_message(
            session, conversation.id, "user", request.message
        )

        # Get conversation history for the agent
        conversation_history = []
        messages = message_service.get_messages_by_conversation(session, conversation.id)
        for msg in messages:
            conversation_history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Process the message with the AI agent
        result = agent_service.process_conversation(
            user_id=user_id,
            user_message=request.message,
            conversation_history=conversation_history[:-1]  # Exclude the current message
        )

        # Save the AI's response to the database
        ai_message = message_service.create_message(
            session, conversation.id, "assistant", result["response"]
        )

        # Update the conversation's timestamp
        message_service.update_conversation_timestamp(session, conversation.id)

        # Log the interaction
        log_chat_interaction(user_id, conversation.id, request.message, result["response"])

        # Calculate API call duration
        duration = (datetime.now() - start_time).total_seconds()
        log_api_call(f"/api/{user_id}/chat", user_id, duration, status.HTTP_200_OK)

        return ChatResponse(
            conversation_id=conversation.id,
            response=result["response"],
            tool_calls=result.get("tool_calls", [])
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Calculate API call duration for error case
        duration = (datetime.now() - start_time).total_seconds()
        log_error(e, f"Chat endpoint for user {user_id}")
        log_api_call(f"/api/{user_id}/chat", user_id, duration, status.HTTP_500_INTERNAL_SERVER_ERROR)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )