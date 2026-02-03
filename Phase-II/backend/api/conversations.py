from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from db.database import get_session
from models.conversation_model import Conversation, ConversationCreate, ConversationResponse, Message, MessageCreate, MessageResponse, RoleEnum
from auth.jwt_dependency import get_current_user, User

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new conversation for the authenticated user"""
    db_conversation = Conversation(
        user_id=current_user.id
    )

    session.add(db_conversation)
    session.commit()
    session.refresh(db_conversation)

    return db_conversation


@router.get("/", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all conversations for the authenticated user"""
    statement = select(Conversation).where(Conversation.user_id == current_user.id)
    conversations = session.exec(statement).all()

    return conversations


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific conversation by ID for the authenticated user"""
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    )
    conversation = session.exec(statement).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversation


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def create_message(
    conversation_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new message in a conversation"""
    # Verify that the conversation belongs to the authenticated user
    conversation_statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    )
    conversation = session.exec(conversation_statement).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Verify that the conversation_id matches
    if message.conversation_id != conversation_id:
        raise HTTPException(status_code=400, detail="Conversation ID mismatch")

    db_message = Message(
        conversation_id=message.conversation_id,
        user_id=current_user.id,
        role=message.role,
        content=message.content
    )

    session.add(db_message)
    session.commit()
    session.refresh(db_message)

    return db_message


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all messages for a specific conversation"""
    # Verify that the conversation belongs to the authenticated user
    conversation_statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    )
    conversation = session.exec(conversation_statement).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    messages = session.exec(statement).all()

    return messages