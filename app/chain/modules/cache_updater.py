from typing import Any
from loguru import logger
from app.base.abstract_handlers import AbstractHandler

class Cacheupdater(AbstractHandler):
    """
    A handler class for updating the cache with new query responses.

    This class extends AbstractHandler and provides functionality to update
    the cache with new question-inference pairs when appropriate.
    """

    def __init__(self,Cachestore) -> None:
        """
        Initialize the Cacheupdater.

        Args:
            Cachestore (Any): The cache storage mechanism.
        """
        self.cache = Cachestore

    def handle(self, response: Any) -> str:
         """
        Handle the incoming response by updating the cache if necessary.

        Args:
            response (Dict[str, Any]): The response to be processed.

        Returns:
            str: The response after processing.
        """
        logger.info("passing through => cache_updater")
        data = response["query_response"]

        # question would not be in response if retrieved from cache
        if ("question" in response) and not(data is None or len(data) == 0):
            logger.info("cache updated")
            inference = response["inference"]
            question = response["question"]
            self.cache.update_cache(
                document = question,
                metadata = inference,
            )
        return super().handle(response)