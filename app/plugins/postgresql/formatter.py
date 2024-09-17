from typing import Any, Optional
import re
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
            response = self.BasicFormatter(data, input)
        elif self.kind == "aggregation":
            response = self.AggregationFormatter(data, input)

        response["main_entity"] = self.main_entity
        response["main_format"] = self.kind
        response["role"] = "assistant"
        response["content"] = self.general_message
        
        return response
    
    def BasicFormatter(self, data: Any, input:Any) -> dict :
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
    
    
    def AggregationFormatter(self, data:Any, input:Any) -> dict :
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
    
    def DefaultFormatter(self, data:Any, input:Any) -> dict :
        response = {}
        if data is None or len(data) == 0:
            response["data"] = []
            response["kind"] = "none"
        else:
            if input["operation_kind"] == "list":
                response["kind"] = "table"
                response["data"] = data
            else:
            
                out_structure = self.filter_aggregated_value_fields(data[0])
            
                if len(out_structure["values"]) == 1 and len(out_structure["labels"]) > 0:
                    
                    processed_data = []
                    for single in data:
                        processed_data.append({ 
                            "labels": {key:single[key] for key in out_structure["labels"]},
                            "value" : single[out_structure["values"][0]],
                            "metric": out_structure["values"][0],
                        })
                    
                    if self.main_entity == "service":
                        response["data"] = processed_data
                        response["kind"] = "card_list"
                    elif len(data) <= 5 and len(data) > 1:
                        response["data"] = processed_data
                        response["kind"] = "pie_chart"
                    else:
                        response["data"] = processed_data
                        response["kind"] = "pie_chart"
                else:
                    response["kind"] = "table"
                    response["data"] = data
                    
        return response
    
    def filter_aggregated_value_fields(self, data):
        keys = data.keys()
        
        prefix_match = re.compile('(?:average|total|max|min|maximum|minimum|mean)(\\w+)')
        suffix_match = re.compile('(\\w+)(?:count|sum)')
        
        prefix_keys = []
        suffix_keys = []
        for key in keys:
            p_matches  = prefix_match.findall(key)
            s_matches =  suffix_match.findall(key)
            if len(s_matches) > 0 or len(p_matches)> 0:
                suffix_keys.append(key)
        
        values = list(set().union(prefix_keys, suffix_keys))
        labels = list(keys - values)
        
        out ={}
        out["labels"] = labels if len(labels) > 0 else []
        out["values"] = values if len(values) > 0 else []

        return out
        
    
        
