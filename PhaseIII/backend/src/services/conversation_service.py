from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate
from datetime import datetime
from typing import List, Optional


class ConversationService:
    """
    Service class for handling conversation and message operations
    """

    def create_conversation(self, session: Session, user_id: str) -> Conversation:
        """
        Create a new conversation for a user
        """
        conversation = Conversation(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, session: Session, conversation_id: int) -> Optional[Conversation]:
        """
        Retrieve a conversation by its ID
        """
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    def get_conversations_by_user(self, session: Session, user_id: str) -> List[Conversation]:
        """
        Retrieve all conversations for a specific user
        """
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()


class MessageService:
    """
    Service class for handling message operations
    """

    def create_message(self, session: Session, conversation_id: int, role: str, content: str) -> Message:
        """
        Create a new message in a conversation
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def get_messages_by_conversation(self, session: Session, conversation_id: int) -> List[Message]:
        """
        Retrieve all messages in a conversation
        """
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
        return session.exec(statement).all()

    def update_conversation_timestamp(self, session: Session, conversation_id: int):
        """
        Update the updated_at timestamp for a conversation
        """
        conversation = self.get_conversation_by_id(session, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()