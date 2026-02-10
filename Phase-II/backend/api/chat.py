import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Dict, Any, List
import json
from datetime import datetime
from db.database import get_session
from models.conversation_model import Conversation, Message, MessageCreate, RoleEnum
from models.task_model import Task
from auth.jwt_dependency import get_current_user, User
from service_agents.todo_agent import TodoAgent

# Configure logging for audit trails
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize the AI agent
todo_agent = TodoAgent()


@router.post("/")
async def chat_endpoint(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint for the AI agent

    Request body:
    - conversation_id (optional): ID of existing conversation
    - message (required): User's message

    Response:
    - conversation_id: ID of the conversation
    - assistant_response: AI's response
    - tool_calls (if any): Information about tools called
    """
    conversation_id = request.get("conversation_id")
    user_message = request.get("message")

    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Log the incoming request for audit trail
    logger.info(f"Chat request received: user_id={current_user.id}, conversation_id={conversation_id}")

    # Get or create conversation
    if conversation_id:
        # Verify that the conversation belongs to the authenticated user
        conversation_stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        conversation = session.exec(conversation_stmt).first()

        if not conversation:
            logger.warning(f"Conversation not found for user {current_user.id}: {conversation_id}")
            raise HTTPException(status_code=404, detail="Conversation not found")

        logger.info(f"Using existing conversation: {conversation_id} for user {current_user.id}")
    else:
        # Create new conversation
        conversation = Conversation(user_id=current_user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        conversation_id = conversation.id
        logger.info(f"Created new conversation: {conversation_id} for user {current_user.id}")

    # Save user message
    user_msg = Message(
        conversation_id=conversation_id,
        user_id=current_user.id,
        role=RoleEnum.user,
        content=user_message
    )
    session.add(user_msg)
    session.commit()
    logger.info(f"Saved user message to conversation {conversation_id}")

    # Process the message with AI agent
    assistant_response, tool_calls = await todo_agent.process_message(
        current_user.id,
        user_message,
        session
    )

    # Save assistant message
    assistant_msg = Message(
        conversation_id=conversation_id,
        user_id=current_user.id,  # The assistant acts on behalf of the user
        role=RoleEnum.assistant,
        content=assistant_response
    )
    session.add(assistant_msg)
    session.commit()
    logger.info(f"Saved assistant response to conversation {conversation_id}")

    # Update conversation timestamp
    conversation.updated_at = datetime.now()
    session.add(conversation)
    session.commit()

    # Log tool calls for audit trail
    if tool_calls:
        logger.info(f"Tool calls executed for user {current_user.id} in conversation {conversation_id}: {[call['tool_name'] for call in tool_calls]}")

    logger.info(f"Chat request completed: user_id={current_user.id}, conversation_id={conversation_id}")

    return {
        "conversation_id": conversation_id,
        "assistant_response": assistant_response,
        "tool_calls": tool_calls
    }