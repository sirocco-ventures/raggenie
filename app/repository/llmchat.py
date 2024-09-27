from sqlalchemy.orm import Session
from app.models.llmchat import ChatHistory
from app.schemas import llmchat as schemas
from sqlalchemy.exc import SQLAlchemyError



def get_chat_by_context_and_id(chat_context_id: str, chat_id: int, db: Session):
    try:
        chat = db.query(ChatHistory).filter(ChatHistory.chat_context_id == chat_context_id, ChatHistory.chat_id == chat_id).first()
        return chat, False
    except SQLAlchemyError as e:
        return e, True

def create_new_chat(chat: schemas.ChatHistoryCreate, db: Session):
    try:
        existing_chat = db.query(ChatHistory).filter(ChatHistory.chat_context_id == chat.chat_context_id).first()

        chat.primary_chat=existing_chat is None

        db_chat = ChatHistory(
            **chat.model_dump()
        )

        db.add(db_chat)
        db.commit()
        db.refresh(db_chat)
        return db_chat, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

# based on feedback
def update_chat_feedback(feedback: schemas.FeedbackCreate, db: Session):
    chat, is_error = get_chat_by_context_and_id(feedback.chat_context_id, feedback.chat_id, db)
    if is_error:
        return chat, True

    if not chat:
        return None, False

    chat.feedback_status = feedback.feedback_status
    chat.feedback_json = feedback.feedback_json

    try:
        db.commit()
        db.refresh(chat)
        return chat, False
    except SQLAlchemyError as e:
        return e, True


def get_primary_chat(db: Session):
    try:
        data = db.query(ChatHistory).filter(ChatHistory.primary_chat == True).distinct(ChatHistory.chat_context_id).all()
        return data, False
    except SQLAlchemyError as e:
        return e, True


def get_all_chats_by_context_id(context_id: str, db: Session):
    try:
        data = db.query(ChatHistory).filter(ChatHistory.chat_context_id == context_id).all()
        return data, False
    except SQLAlchemyError as e:
        return e, True