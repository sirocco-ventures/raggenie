from pydantic import BaseModel
from  typing import Dict,List, Literal
from typing import Any


class Chat(BaseModel):
    content: str
    role: str


class FlowItem(BaseModel):
    question: str
    answer: dict

class PostBody(BaseModel):
    question: str
    flow: list[FlowItem]

class ResponseItem(BaseModel):
    description: str
    metadata: Dict[str,str]

class FeedbackCorrectionRequest(BaseModel):
    responses: List[ResponseItem]


class ConnectionArgument(BaseModel):
    type: Literal[1,2,3,4,6,7, 8]
    generic_name: str
    description: str
    order: int
    required: bool
    value: Any
    slug: str