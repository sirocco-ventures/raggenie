from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from app.models.request import Chat, FeedbackCorrectionRequest
from starlette.requests import Request
from loguru import logger
from app.schemas import llmchat as schemas
from app.api.v1 import llmchat
from sqlalchemy.orm import Session
from app.utils.database import get_db


MainRouter = APIRouter()


@MainRouter.post("/query", status_code=status.HTTP_201_CREATED)
async def qna(query: Chat, request: Request, background_tasks: BackgroundTasks, db:Session = Depends(get_db)):

    """
    Handles user queries and invokes the chain to get an answer from the LLM.

    Args:
        query (Chat): User query as a Chat model.
        request (Request): FastAPI request object containing context and app-level dependencies.
        background_tasks (BackgroundTasks): Background task for asynchronous logging.
        db (Session): Database session dependency.

    Returns:
        dict: Response containing the answer to the user's query and the original query text.
    """

    context_id = request.headers.get('x-llm-context-id')
    user_id = request.headers.get('x-llm-user-id')

    logger.info(f"{context_id} - {user_id} - query: {query.content}")


    out = await request.app.chain.invoke({
        "question": query.content,
        "context_id": context_id,
    })

    resp = llmchat.create_chat(
        schemas.ChatHistoryCreate(
            chat_context_id=context_id,
            chat_query=query.content,
            chat_answer= jsonable_encoder(out),
            chat_summary=out.get("summary", query.content)
        ),
        db
    )

    if resp.status:
        out["chat_id"] = resp.data["chat"].chat_id


    return {
        "response": out,
        "query": query.content,
    }


#! This api is not in use right now, instead we are using a scheduler for the feedback_correction job
@MainRouter.post("/feedback_correction", status_code=status.HTTP_201_CREATED)
def feedback_correction(request: Request, body: FeedbackCorrectionRequest):

    """
    Processes feedback from LLM responses and updates the vector store accordingly.

    Args:
        request (Request): FastAPI request object containing the app's vector store.
        body (FeedbackCorrectionRequest): Request body containing user feedback to be processed.

    Returns:
        str: Success message indicating the feedback processing outcome.

    """

    store = request.app.vector_store

    if body.responses:
        for response in body.responses:
            similar_sample = store.find_similar_samples(response.description)
            if len(similar_sample) > 0 and similar_sample[0]['distances'] < 0.3:
                store.update_store(similar_sample[0]['id'],response.metadata,response.description)
            else:
                store.update_store(metadatas = response.metadata,documents = response.description)
        return "Success: Feedback received and processed."

    else:
        return "Success: No Feedback received and processed."


