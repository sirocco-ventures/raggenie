from typing import Any
from loguru import logger


class Formatter:
    def format(self, data: Any,input) -> (dict):
        """
        Main entry point for formatting the data based on the input parameters.
        Handles different formatting strategies based on operation kind.

        :param data: The data to format.
        :param input_params: Dictionary containing operation and formatting details.
        :return: A dictionary containing the formatted response.
        """
        response = {}
        self.main_entity = input.get("main_entity")
        self.kind = input.get("operation_kind", "").lower()
        self.general_message = input.get("general_message")
        self.empty_message = input.get("empty_message")

        logger.info("Formatting output using inference for sqlite")

        if self.kind  == "list":
            response = self.basic_formatter(data, input)
        elif self.kind == "aggregation":
            response = self.aggregation_formatter(data, input)
        else:
            response["data"] = data
            response["kind"] = "list"


        response.update({
            "main_entity": self.main_entity,
            "main_format": self.kind,
            "role": "assistant",
            "content": self.general_message,
            "empty_message": self.empty_message,
        })

        return response

    def basic_formatter(self, data: Any, input:Any) -> dict :
        """
        Formats data as a list, handling cases for none, single, and multiple entries.

        :param data: The data to format.
        :return: A dictionary containing the formatted list response.
        """
        logger.info("Formatting data as a list")

        if data is None:
            response = {"data": [], "kind": "none"}
        elif len(data) == 1:
            response = {"data": data, "kind": "single"}
        else:
            response = {"data": data, "kind": "list"}

        return response


    def aggregation_formatter(self, data:Any, input:Any) -> dict :
        """
        Formats data for aggregation visualisation, supporting table and chart formats.

        :param data: The data to format.
        :param visualisation: Dictionary containing visualisation details (e.g., x-axis, y-axis, chart type).
        :return: A dictionary containing the formatted aggregation response.
        """

        logger.info("Formatting data as aggregation")

        visualisation = input.get("visualisation", {})
        title = visualisation.get("title", "")
        response = {}


        if data is None or len(data) == 0:
            response = {"data": [], "kind": "none"}
        elif len(data) == 1:
            response = {"data": data, "kind": "table", "title": title}
        else:
            value_fields = visualisation.get("y-axis", [])
            key_fields = visualisation.get("x-axis", [])

            visualisaton_kind = visualisation["type"].replace(" ", "_") if visualisation["type"] is not None else "table"

            if visualisaton_kind.lower() in ["bar_chart", "line_chart", "pie_chart"] and len(value_fields) > 0 and len(key_fields) > 0:
                response["kind"] = visualisaton_kind
                response["data"] = data
                response["x"] = key_fields
                response["y"] = value_fields
                response["title"] = title
            else:
                response = {"kind": "table", "data": data, "title": title}

        return response
