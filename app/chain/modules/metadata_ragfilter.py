from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger


class MetadataRagFilter(AbstractHandler):
    """
    A handler for applying RAG (retrieval-augmented generation) filters based on metadata.

    This class modifies the request's response to include RAG filters, setting the number of documents and schemas
    to be considered in retrieval operations. It also includes tracing for monitoring and debugging purposes.

    Inherits from:
        AbstractHandler: A base class for handling requests in the application.

    Methods:
        handle(request: Any) -> str:
            Processes the request to apply RAG filters and forwards it to the next handler.
    """

    def handle(self, request: Any) -> str:
        """
        Applies RAG filters to the request's response and forwards it to the next handler.

        Args:
            request (Any): The incoming request containing the necessary information for filtering.

        Returns:
            str: The result of the superclass's handle method with updated response information.
        """
        logger.info("passing through => metadata_ragfilter")
        response = request
        response["rag_filters"] = {
                "datasources": response.get("available_datasources", []),
                "document_count": 50,
                "schema_count": 10
        }


        return super().handle(response)
