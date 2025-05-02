from typing import Any
from loguru import logger
from app.base.abstract_handlers import AbstractHandler


class Cachechecker(AbstractHandler):
    """
    A handler class for checking and managing cache operations.

    This class extends AbstractHandler and provides functionality to check
    if a query exists in the cache and handle the response accordingly.
    """

    def __init__(self,common_context, cachestore, forward_handler, forward: bool = True) -> None:
        """
        Initialize the Cachechecker.

        Args:
            common_context: The common context shared across handlers.
            Cachestore: The cache storage mechanism.
            forward_handler: The next handler in the chain.
            forward (bool): Whether to forward the request to the next handler.
        """
        self.cache = cachestore
        self.forward_handler = forward_handler
        self.forward = forward
        self.common_context = common_context


    async def handle(self, request: Any) -> str:
        """
        Handle the incoming request by checking the cache

        Args:
            request (Any): The incoming request to be processed.

        Returns:
            str: The response after processing the request.
        """
        logger.info("passing through => cache_checker")

        response = request
        question = request.get("question", "")
        rag_filters = response["rag_filters"]["datasources"]
        output = await self.cache.find_similar_cache(rag_filters, question)
        if "rag" not in response:
            response["rag"] = {
                "suggestions": output
            }
        else:
            response["rag"]["suggestions"] = output



        if self.forward and len(output) > 0:
            if output[0]["distances"] < -10:
                result = output[0]["metadatas"]
                logger.info("query retrieved from cache")
                return await self.forward_handler.handle({"inference":result})

        logger.info("query not retrieved from cache")
        return await super().handle(response)
