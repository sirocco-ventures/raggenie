# src/endpoints/chat.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import app.schemas.common as resp_schemas
from app.schemas import llmchat as schemas
from app.utils.database import get_db
from app.services import llmchat as svc
import app.api.v1.commons as commons

chat_router = APIRouter()

# Create a new chat
@chat_router.post("/create", response_model=resp_schemas.CommonResponse)
def create_chat(chat: schemas.ChatHistoryCreate, db: Session = Depends(get_db)):
    result, error = svc.create_chat(chat, db)

    if error:
        return commons.is_error_Response("DB Error", result, {"chat": {}})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        data={"chat": result},
        message="Chat created successfully",
        error=None
    )

# Create feedback for a chat
@chat_router.post("/feedback/create", response_model=resp_schemas.CommonResponse)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    result, error = svc.create_feedback(feedback, db)

    if error:
        return commons.is_error_Response("DB Error", result, {"chat": {}})
    
    if not result:
        return commons.is_None_Reponse("Chat Not Found", {"chat": {}})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"chat": result},
        message="Feedback updated successfully",
        error=None
    )

# List the primary chat based on context
@chat_router.get("/list/context/all", response_model=resp_schemas.CommonResponse)
def list_chat_by_context(db: Session = Depends(get_db)):
    result, error = svc.list_chats_by_context(db)

    if error:
        return commons.is_error_Response("DB Error", error, {"chats": []})
    
    if not result:
        return commons.is_None_Reponse("Context Not found", {"chat": {}})
        
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"chats": result},
        message="Primary chats found",
        error=None
    )

# Get a specific chat by context ID
@chat_router.get("/get/{context_id}", response_model=resp_schemas.CommonResponse)
def get_chat_by_context(context_id: str, db: Session = Depends(get_db)):
    result, error = svc.list_all_chats_by_context_id(context_id, db)

    if error:
        return commons.is_error_Response("DB Error", error, {"chats": []})
    
    if not result:
        return commons.is_None_Reponse("Chat not found", {"chats": []})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"chats": result},
        message="Chat found",
        error=None
    )
