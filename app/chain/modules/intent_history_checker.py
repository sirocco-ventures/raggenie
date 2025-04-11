from app.base.abstract_handlers import AbstractHandler
from typing import Any
from app.providers.config import configs
from string import Template
from app.chain.formatter.general_response import Formatter
from loguru import logger

class IntentHistoryChecker(AbstractHandler):

    def __init__(self, common_context , model_configs, datasources, capability_handler) -> None:

        self.model_configs = model_configs
        self.common_context = common_context
        self.datasources = datasources
        self.capability_handler = capability_handler


    def handle(self, request: Any) -> str:
        logger.info("passing through => Intent history checker")

        response = request
        logger.info(f"response:{response}")

        contexts = request.get("context", [])
        contexts = contexts[-5:] if len(contexts) >= 5 else contexts
        previous_intent = contexts[-1].chat_answer.get("intent", "None") if len(contexts) > 0 else "None"
        missing_params  = contexts[-1].chat_answer.get("inference", {}).get("missing_params", []) if len(contexts) > 0 else []
        intent_abort = contexts[-1].chat_answer.get("inference", {}).get("abort", "false") if len(contexts) > 0 else "false"

        request.update({"intent_extractor": {"intent" : previous_intent}})
        if len(missing_params) > 0 and str(intent_abort).lower() != "true":
            logger.info(f"capability action is not finished!!")
            return self.capability_handler.invoke(request)

        return super().handle(response)
