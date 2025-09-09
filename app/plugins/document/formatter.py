from typing import Any, Dict
from loguru import logger

class Formatter:
    """
    Formatter class to format the response based on the inference and data.
    """


    def format(self, data: Any, inference) -> (dict):
        """
        Format the response using the given data and inference information.

        :param data: The data containing records to process.
        :param inference: Inference details including main entity and operation kind.
        :return: Formatted response dictionary.
        """

        logger.info("Processing output using inference details")

        response = {}
        self.main_entity = inference.get("main_entity", "")
        self.kind = inference.get("operation_kind", "")
        self.general_message = inference.get("general_message", "Unable to process question, try again")
        
        if self.kind == "list":
            response = self.basic_formatter(inference)

        response.update({
            "main_entity": self.main_entity,
            "main_format": self.kind,
            "role": "assistant",
            "content": self.general_message,
        })

        return response


    def basic_formatter(self, input:Any) -> dict :
        """
        Formats data as a list, handling cases for none.

        :param input: The data to format.
        :return: A dictionary containing the formatted list response.
        """
        data = input.get('visualisation', {}).get("image_data", [])

        if data is None:
            response = {"data": [], "kind": "none"}
        else:
            response = {"data": data, "kind": "image"}

        return response