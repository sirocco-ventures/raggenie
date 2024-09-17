from fastapi import APIRouter, Depends, status, BackgroundTasks
from app.models.request import Chat, PostBody, FeedbackCorrectionRequest
from starlette.requests import Request
from loguru import logger
import uuid
from app.schemas import llmchat as schemas
from typing import List
from app.api.v1 import llmchat
from sqlalchemy.orm import Session
from app.utils.database import get_db


MainRouter = APIRouter()


def write_log(trace_id: str, context_id: str, chat_id: str, user_id: str, query: str , request: any):

    logger.info("parellel logging")

    common_context = request.app.chain.common_context
    common_metrics = request.app.metrics_chain.invoke({
            "question": query,
            "prompt_mode": common_context["prompt_mode"],
            "rag": common_context["rag"],
            "inference": common_context["inference_raw"],
            "prompt": common_context["prompt"]
        })
    logger.info(f"common_context:{common_context}")
    logger.info(f"metrics:{common_metrics}")
    llm = common_context['llm']
    metrics = common_context['metrics']
    spec_metrics = common_metrics['metrics']

    logger.log("ONEPANE", f"{format(trace_id, '032x')} | {context_id} | {chat_id} | {user_id} | /query | {query} | {llm['response']['name']} | {llm['input_tokens']} | {llm['output_tokens']} | {llm['total_cost']} | {llm['latency']} | {metrics['on_topic']} | {metrics['toxicity']} | {metrics['llm_security']} | {spec_metrics['faithfulness']} | {spec_metrics['question_profanity']} | {spec_metrics['response_profanity']} | {spec_metrics['context_relevance']} | {spec_metrics['question_neg_polarity']} | {spec_metrics['response_neg_polarity']} | {spec_metrics['question_pii_content']} | {spec_metrics['response_pii_content']} | {metrics['cache']} | {llm['guardrail']['guard']} | {llm['guardrail']['name']} | {llm['guardrail']['input_tokens']} | {llm['guardrail']['output_tokens']} | | {llm['guardrail']['total_cost']} | | {llm['guardrail']['latency']} | {llm['response']['name']} | {llm['response']['response']} | {llm['response']['output_tokens']} | | {llm['response']['total_cost']} | | {llm['response']['latency']}") 


    

@MainRouter.post( "/query", status_code=status.HTTP_201_CREATED )
def qna(query: Chat, request: Request, background_tasks: BackgroundTasks, db:Session = Depends(get_db)):
    
    context_id = request.headers.get('x-llm-context-id')
    user_id = request.headers.get('x-llm-user-id')
    # chat_id = str(uuid.uuid4())

    
    out = request.app.chain.invoke({
        "question": query.content,
        "context_id": context_id,
    })

    resp = llmchat.create_chat(
        schemas.ChatHistoryCreate(
            chat_context_id=context_id,
            chat_query=query.content, 
            chat_answer= out,
            chat_summary=out["summary"]
        ),
        db
    )
    
    if resp.status:
        out["chat_id"] = resp.data["chat"].chat_id
    

    return {
        "response" : out,
        "query": query.content,
    }


#!This api is not using now , intead we are using a scheduler for the feedback_correction job
@MainRouter.post( "/feedback_correction", status_code=status.HTTP_201_CREATED )
def feedback_correction(request: Request, body: FeedbackCorrectionRequest):
    store = request.app.vector_store

    if body.responses:
        for response in body.responses:
            description = response.description
            similar_sample = store.find_similar_samples(response.description)
            if len(similar_sample) > 0 and similar_sample[0]['distances'] < 0.3:
                store.update_store(similar_sample[0]['id'],response.metadata,response.description)
            else:
                store.update_store(metadatas = response.metadata,documents = response.description)
        return "Success: Feedback received and processed."

    else:
        return "Success: No Feedback received and processed."


