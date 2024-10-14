from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger


class OutputFormatter(AbstractHandler):
    """
    A handler for formatting the output based on the provided inference and query responses.

    This class processes the response from a query, formats it based on the available data and inference results,
    and prepares it for further handling. It manages content, context, and additional metadata.

    Attributes:
        common_context (dict): Shared context information used across handlers.
        datasource (dict): A dictionary for data formatting based on the intent.
    """

    def __init__(self,common_context, datasource):
        """
        Initializes the OutputFormatter with common context and datasource.

        Args:
            common_context (dict): Shared context information used across handlers.
            datasource (dict): A dictionary for data formatting based on the intent.
        """
        self.datasource = datasource
        self.common_context = common_context


    def handle(self, request: Any) -> str:
        """
        Formats the response based on the inference and query response.

        Args:
            request (Any): The incoming request containing inference results and query response.

        Returns:
            str: The result of the superclass's handle method with updated response information.
        """

        logger.info("passing through => output_formatter")

        input_data = request.get("inference", {})
        response = {}

        if "main_entity" in input_data and "operation_kind" in input_data :
            intent_key = self.common_context.get("intent")
            if intent_key in self.datasource:
                response = self.datasource[intent_key].format(request.get("query_response"), input_data)
        elif "general_message" in input_data:
            response["content"] = str(input_data.get('general_message'))


        if "data" in response and isinstance(response["data"], list) and len(response["data"]) == 0:
            if  "empty_message" in input_data:
                response["content"] = input_data["empty_message"]
            else:
                response["content"] = "I didn't find any data matching the query"
            response["main_format"] = "general_chat"
        elif "kind" in response and response["kind"] == "none":
            response["content"] = input_data.get("empty_message", "I didn't find any relevant data regarding this, please reframe your query")
            response["main_format"] = "general_chat"


        response["next_questions"] = input_data.get("next_questions", [])

        if "context_id" in request:
            response["context_id"] = request["context_id"]
            response["question"] = request["question"]

        response["query"] = input_data.get("query", '')
        response["summary"] = request.get("summary", '')


        return super().handle(response)
