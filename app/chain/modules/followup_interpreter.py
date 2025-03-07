from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
from app.chain.formatter.general_response import Formatter

class FollowupInterpreter(AbstractHandler):
    """
    A handler class for interpreting follow-up responses and formatting them.

    This class extends AbstractHandler and provides functionality to interpret
    the inference results from follow-up queries and format the response accordingly.
    """


    def __init__(self, common_context, general_chain) -> None:
        """
        Initialize the FollowupInterpreter.

        Args:
            common_context (Dict[str, Any]): The common context shared across handlers.
            general_chain (Any): The general processing chain for fallback scenarios.
        """

        self.common_context = common_context
        self.general_chain = general_chain

    async def handle(self, request: Any) -> str:
        """
        Handle the incoming request by interpreting the inference results and formatting the response.
        Args:
            request (Dict[str, Any]): The incoming request to be processed.

        Returns:
            str: The formatted response after processing the request.
        """

        logger.info("passing through => interpreter")
        response = request

        if "inference" in request:
            inference = request["inference"]
            if inference["completed"] == True or inference["completed"] == "true":
                logger.info("Intent completed, trigger the action")

            response = Formatter.format(inference["message"],"")
            response["summary"] = request["inference"]["summary"]
            response["question"] = request["question"]
            response["context_id"] = request["context_id"]
        else:
            logger.info("No intents detected")
            response = Formatter.format("Sorry, I didn't get that","")

        return await super().handle(response)

