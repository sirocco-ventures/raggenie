from typing import Any
from loguru import logger
from app.base.abstract_handlers import AbstractHandler
from app.models.llmchat import ChatHistory

class ContextRetreiver(AbstractHandler):
    """
    A handler class for retrieving context information for a chat.

    This class extends AbstractHandler and provides functionality to fetch
    relevant context based on the context_id provided in the request.
    """

    def __init__(self,common_context, context_store) -> None:
        """
        Initialize the ContextRetriever.

        Args:
            common_context (Any): The common context shared across handlers.
            context_store (Any): The storage mechanism for context data.
        """
        self.context_store = context_store
        self.common_context = context_store

    def handle(self, request: Any) -> str:
        """
        Handle the incoming request by retrieving relevant context.
        
        Args:
            request (Dict[str, Any]): The incoming request to be processed.

        Returns:
            str: The response after processing the request.
        """

        logger.info("retreiving context into chain")
        response = request
        
        context = []
        
        if "context_id" in request:
            records = self.context_store.query_data(model = ChatHistory, filters= {"chat_context_id": request["context_id"]})
            context.extend(records)

        response["context"] = context
        
        return super().handle(response)
