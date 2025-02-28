from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class ChatHistoryBase(BaseModel):
    chat_context_id: str
    chat_query: str
    chat_answer: dict
    chat_summary: str
    chat_status: Optional[int]=None
    feedback_status: Optional[int]=None
    feedback_json: Optional[dict] = None
    user_id: Optional[int]=None
    primary_chat: Optional[bool]=False
    environment_id: Optional[int]=None

class ChatHistoryCreate(ChatHistoryBase):
    pass


class ChatHistory(ChatHistoryBase):
    chat_id: int


class ChatResponse(ChatHistory):
    created_at: datetime
    updated_at: Optional[datetime] = None

class FeedbackCreate(BaseModel):
    chat_context_id: str
    chat_id: int
    feedback_status: int
    feedback_json: Optional[Dict] = None

class ListPrimaryContext(BaseModel):
    chat_context_id: str
    chat_query: str
    chat_answer: Dict
    user_id: int
    primary_chat: bool
