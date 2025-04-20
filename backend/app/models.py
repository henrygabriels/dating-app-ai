from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime, Boolean, Index, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)  # Clerk user ID
    created_at = Column(DateTime, default=datetime.utcnow)
    conversation_state = Column(JSON, default={})
    scores = Column(JSON, default={})  # Personality/preference scores from LLM conversation
    conversations = relationship("Conversation", back_populates="user")
    
    # Profile fields
    display_name = Column(String)
    bio = Column(String)
    age = Column(Integer)
    gender = Column(String)
    location = Column(String)
    preferences = Column(JSON, default={})  # Matching preferences
    
    # Relationships
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.recipient_id", back_populates="recipient")
    
    # Indexes for efficient filtering
    __table_args__ = (
        Index('idx_user_location', 'location'),
        Index('idx_user_age', 'age'),
        Index('idx_user_gender', 'gender'),
    )

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(String, primary_key=True)
    original_text = Column(String, nullable=False)
    category = Column(String, nullable=False)
    weight = Column(Float, default=1.0)

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)
    history = Column(JSON, default=[])
    user = relationship("User", back_populates="conversations")

class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    question_id = Column(String, ForeignKey("questions.id"))
    response_text = Column(String, nullable=False)
    extracted_data = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    sender_id = Column(String, ForeignKey("users.id"))
    recipient_id = Column(String, ForeignKey("users.id"))
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")
    
    __table_args__ = (
        Index('idx_message_sender', 'sender_id'),
        Index('idx_message_recipient', 'recipient_id'),
        Index('idx_message_created', 'created_at'),
    )