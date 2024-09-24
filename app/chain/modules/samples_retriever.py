from app.base.abstract_handlers import AbstractHandler
from loguru import logger
from typing import Any


class SamplesRetriever(AbstractHandler):
    """
    A handler for retrieving similar samples from a store based on the provided question.

    This class queries the store for samples similar to the input question and updates the response with the
    retrieved suggestions and their scores.

    Attributes:
        store (object): The data store used to find similar samples.
    """

    def __init__(self,store):
        """
        Initializes the SamplesRetriever with the provided store.

        Args:
            store (object): The data store used to find similar samples.
        """
        self.store =store

    def handle(self, request: Any) -> str:
        """
        Retrieves similar samples from the store and updates the response with the results.

        Args:
            request (Any): The incoming request containing the question for sample retrieval.

        Returns:
            Dict[str, Any]: The updated response dictionary with retrieved suggestions and their scores.
        """
        logger.info("passing through => samples_retriever")
        response = request


        question = request.get("question", "")

        similar_samples = self.store.find_similar_samples(question)

        if similar_samples:
            response = {
                "rag": {
                    "suggestions": similar_samples,
                    "suggestions_score": ""
                }
            }
        else:
            response = {
                "rag": {
                    "suggestions": [],
                    "suggestions_score": ""
                }
            }

        return response




