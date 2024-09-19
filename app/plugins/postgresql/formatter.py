from typing import Any
from loguru import logger
class Formatter:

    def format(self, data: Any,input:Any) -> (dict, Any):
        response = {}


        self.main_entity = input["main_entity"]
        self.kind = input["operation_kind"]
        self.visualisation = input["visualisation"] if "visualisation" in input else {}
        self.general_message = input["general_message"]

        logger.info("from postgres formatter module")
        if self.kind  == "list":
            response = self.basic_formatter(data, input)
        elif self.kind == "aggregation":
            response = self.aggregation_formatter(data, input)

        response["main_entity"] = self.main_entity
        response["main_format"] = self.kind
        response["role"] = "assistant"
        response["content"] = self.general_message

        return response

    def basic_formatter(self, data: Any, input:Any) -> dict :
        logger.info("basic formatter")


        response = {

        }

        if data is None or len(data) == 0:
            response["data"] = []
            response["kind"] = "none"
        elif len(data) == 1:
            response["data"] = data[0]
            response["kind"] = "single"
        else:
            response["data"] = data
            response["kind"] = "list"


        return response


    def aggregation_formatter(self, data:Any, input:Any) -> dict :
        response = {}

        if data is None or len(data) == 0:
            response["data"] = []
            response["kind"] = "none"

        else:
            visualisaton = input["visualisation"]
            if visualisaton["chart"] == "none":
                response["kind"] = "table"
                response["data"] = data
            else:

                value_fileds = visualisaton["y-axis"]
                key_fields = visualisaton["x-axis"]
                visualisaton_kind = visualisaton["chart"].replace(" ", "_")


                if visualisaton_kind in ["bar_chart", "line_chart", "pie_chart"]:
                    processed_data = []

                    for single in data:
                        for value_field in value_fileds:

                            labels = key_fields

                            for k in single.keys():
                                if k not in key_fields and k not in value_field:
                                    labels.append(k)

                            processed_data.append({
                                "labels": {key:single[key] for key in  key_fields},
                                "value" : single[value_field],
                                "metric": value_field,
                                })
                    # if self.main_entity == "service":
                    #     response["kind"] = "card_list"
                    # else:
                    #     response["kind"] = visualisaton_kind
                    response["kind"] = visualisaton_kind
                    response["data"] = processed_data
                else:
                    response["kind"] = "table"
                    response["data"] = data

        return response
