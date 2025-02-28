from sqlalchemy.orm import Session
from app.repository import llmchat as repo
from app.schemas import llmchat as schemas


def create_chat(chat: schemas.ChatHistoryCreate, db: Session):

    """
    Creates a new chat record in the database.

    Args:
        chat (schemas.ChatHistoryCreate): Data required to create a new chat.
        db (Session): Database session object.

    Returns:
        Tuple: Chat history schema and error message (if any).
    """

    result, is_error = repo.create_new_chat(chat, db)

    if is_error:
        return result, "DB Error"

    data = schemas.ChatHistory(
        chat_context_id=result.chat_context_id,
        chat_answer=result.chat_answer,
        chat_id=result.chat_id,
        chat_query=result.chat_query,
        chat_status=result.chat_status,
        chat_summary=result.chat_summary,
        primary_chat=result.primary_chat,
        feedback_json=result.feedback_json,
        feedback_status=result.feedback_status,
        user_id=result.user_id
    )

    return data, None


def create_feedback(feedback: schemas.FeedbackCreate, db: Session):

    """
    Updates an existing chat record with feedback data.

    Args:
        feedback (schemas.FeedbackCreate): Feedback data to update the chat record.
        db (Session): Database session object.

    Returns:
        Tuple: Updated chat history schema and error message (if any).
    """

    result, is_error = repo.update_chat_feedback(feedback, db)

    if is_error:
        return result, "DB Error"

    if result is None:
        return [], None

    data = schemas.ChatHistory(
        chat_context_id=result.chat_context_id,
        chat_answer=result.chat_answer,
        chat_id=result.chat_id,
        chat_query=result.chat_query,
        chat_status=result.chat_status,
        chat_summary=result.chat_summary,
        primary_chat=result.primary_chat,
        feedback_json=result.feedback_json,
        feedback_status=result.feedback_status,
        user_id=result.user_id
    )

    return data, None


def list_chats_by_context(env_id: int, db: Session):

    """
    Retrieves the primary chat records from the database.

    Args:
        db (Session): Database session object.

    Returns:
        Tuple: List of chat responses and error message (if any).
    """

    result, is_error = repo.get_primary_chat(env_id, db)

    if is_error:
        return result, "DB Error"

    if not result:
        return [], None

    chat_data = [
        schemas.ChatResponse(
            chat_context_id=chat.chat_context_id,
            chat_answer=chat.chat_answer,
            chat_id=chat.chat_id,
            chat_query=chat.chat_query,
            chat_status=chat.chat_status,
            chat_summary=chat.chat_summary,
            primary_chat=chat.primary_chat,
            feedback_json=chat.feedback_json,
            feedback_status=chat.feedback_status,
            user_id=chat.user_id,
            created_at=chat.created_at,
            updated_at=chat.updated_at
        ) for chat in result
    ]

    return chat_data, None


def list_all_chats_by_context_id(context_id: str, db: Session):

    """
    Retrieves all chat records based on the context ID from the database.

    Args:
        context_id (str): The ID of the context to filter chats.
        db (Session): Database session object.

    Returns:
        Tuple: List of chat responses and error message (if any).
    """

    result, is_error = repo.get_all_chats_by_context_id(context_id, db)

    if is_error:
        return result, "DB Error"

    if not result:
        return [], None

    chat_data = [
        schemas.ChatResponse(
            chat_context_id=chat.chat_context_id,
            chat_answer=chat.chat_answer,
            chat_id=chat.chat_id,
            chat_query=chat.chat_query,
            chat_status=chat.chat_status,
            chat_summary=chat.chat_summary,
            primary_chat=chat.primary_chat,
            feedback_json=chat.feedback_json,
            feedback_status=chat.feedback_status,
            user_id=chat.user_id,
            created_at=chat.created_at,
            updated_at=chat.updated_at
        ) for chat in result
    ]

    return chat_data, None

