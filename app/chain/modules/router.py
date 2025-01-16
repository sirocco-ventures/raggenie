from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
from app.chain.formatter.general_response import Formatter


class Router(AbstractHandler):
    """
    A handler that routes requests to appropriate handlers based on the detected intent.

    The Router class determines the correct handler to process the request based on the intent extracted
    from the request. It forwards the request to the appropriate handler or returns a fallback response
    if no suitable handler is found.

    Attributes:
        fallback_handler (AbstractHandler): Handler to process requests that do not match any specific intent.
        general_handler (AbstractHandler): Handler for general intent processing.
        capability_handler (AbstractHandler): Handler for capability-related intents.
        metadata_handler (AbstractHandler): Handler for metadata-related intents.
    """


    def __init__(self, common_context, fallback_handler, intent_handler, general_handler, capability_handler, metadata_handler) -> None:
        """
        Initializes the Router with the provided handlers.

        Args:
            common_context (dict): Shared context information used across handlers.
            fallback_handler (AbstractHandler): Handler for fallback responses.
            general_handler (AbstractHandler): Handler for general intent processing.
            capability_handler (AbstractHandler): Handler for capability-related intents.
            metadata_handler (AbstractHandler): Handler for metadata-related intents.
        """

        self.fallback_handler = fallback_handler
        self.forwared_handler = intent_handler
        self.general_handler = general_handler
        self.capability_handler = capability_handler
        self.metadata_handler = metadata_handler


    def handle(self, request: Any) -> str:
        """
        Routes the request to the appropriate handler based on the detected intent.


        Args:
            request (Any): The incoming request containing intent information.

        Returns:
            str: The result of the handled request.
        """

        logger.info("passing through => Router")
        response = request

        intent_extractor = request.get("intent_extractor", {})
        intent = intent_extractor.get("intent", "")

        if intent:
            if intent in  self.forwared_handler.data_sources:
                datasource = self.forwared_handler.data_sources[intent]

                if datasource.__category__ == 4:
                    logger.info("entered database workflow")
                    return super().handle(self.forwared_handler.invoke(request))
                else:
                    logger.info("entered default workflow")
                    return super().handle(self.general_handler.invoke(request))

            elif intent == "metadata_inquiry":
                return super().handle(self.metadata_handler.invoke(request))
            elif intent in request.get("available_intents", []) and intent != "out_of_context":
                return super().handle(self.capability_handler.invoke(request))
            else:
                response = Formatter.format("Sorry, I can't help you with that. Is there anything i can help you with ?","")
                return self.fallback_handler.handle(response)

        else:
            logger.info("No intents detected")
            response = Formatter.format("Sorry, I can't help you with that. Is there anything i can help you with ?","")
            return self.fallback_handler.handle(response)

