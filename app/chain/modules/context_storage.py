from typing import Any
from loguru import logger
from app.base.abstract_handlers import AbstractHandler
from app.models.db import Chat
import datetime

class ContextStorage(AbstractHandler):
    """
    A handler class for storing chat interactions in the context.

    This class extends AbstractHandler and provides functionality to store
    chat interactions, including questions, answers, and summaries, in the context store.
    """

    def __init__(self,common_context, context_store) -> None:
        """
        Initialize the ContextStorage.

        Args:
            common_context (Any): The common context shared across handlers.
            context_store (Any): The storage mechanism for context data.
        """
        self.context_store = context_store
        self.common_context = context_store

    async def handle(self, request: Any) -> str:
        """
        Handle the incoming request by storing the interaction in the context.

        Args:
            request (Dict[str, Any]): The incoming request to be processed.

        Returns:
            str: The response after processing the request.
        """

        logger.info("Storing interaction into context")
        response = request

        summary = ''
        if "summary" in request:
            summary = request['summary']
        if "context_id" in request:
            self.context_store.insert_data(Chat(context_id = request["context_id"], question = request["question"], created_at = datetime.datetime.now(), answer = request["content"], summary = summary))

        return await super().handle(response)
