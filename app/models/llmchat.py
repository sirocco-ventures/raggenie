from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class ChatHistory(Base):
    __tablename__ = 'chat_histories'

    chat_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_context_id = Column(String, index=True, nullable=False)
    chat_query = Column(String, nullable=False)
    chat_answer = Column(JSON, nullable=False)
    chat_summary = Column(String, nullable=False)
    chat_status = Column(Integer, nullable=True)
    feedback_status = Column(Integer, nullable=True)
    feedback_json = Column(JSON, nullable=True)
    user_id = Column(Integer, nullable=True)
    primary_chat = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
