from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
from app.chain.formatter.general_response import Formatter
from string import Template
import json

class FollowupInterpreter(AbstractHandler):
    """
    A handler class for interpreting follow-up responses and formatting them.

    This class extends AbstractHandler and provides functionality to interpret
    the inference results from follow-up queries and format the response accordingly.
    """


    def __init__(self, common_context, datasources) -> None:
        """
        Initialize the FollowupInterpreter.

        Args:
            common_context (Dict[str, Any]): The common context shared across handlers.
            general_chain (Any): The general processing chain for fallback scenarios.
        """

        self.common_context = common_context
        self.datasources = datasources

    def handle(self, request: Any) -> str:
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
            capability = request.get("capability",{})
            required_params = capability.get("requirements", [])
            extracted_params = inference.get("params", {})

            missing_params = [param for param in required_params if param["parameter_name"] not in extracted_params]

            if len(missing_params) == 0:
                logger.info("Intent completed, triggering the action")

                inference["abort"] = "true"
                response = Formatter.format(f"{inference['message']} {inference['followup']} ","")
                if inference["completed"] == False or inference["completed"] == "false":
                    response = Formatter.format("The requested process has been successfully completed!","")

                response['params'] = {} if 'params' in response else response.get('params')
                actions = capability.get("action",[])
                if len(actions) == 0:
                    logger.info("No actions are linked with capability")
                
                for action in actions:
                    connector = action.get("connector",{})
                    if connector.get("name","") in self.datasources :
                        datasource = self.datasources[connector.get("name","")]
                        if datasource.__actions_enabled__ :
                        
                            body_string = json.dumps(action.get("body", {}))
                            temp = Template(body_string).safe_substitute(
                                **extracted_params
                            )
                            body = json.loads(temp)
                            action = action.get("action", "")
                            
                            if action in datasource.__actions_supported__:
                                match action:
                                    case "send":
                                        datasource.send(body)
                                    case "default":
                                        logger.warning("unsupported action")
                                        
                            else:
                                logger.warning("unsupoorted action for connector")
                        else:
                            logger.warning("actions are not enabled in connector")
                    else:
                        logger.warning(f"failed to load connector for action {action.get('name','')}")
            else:
                logger.info("missing parameters")
                response = Formatter.format(inference["followup"],"")
                if inference["abort"] == True or inference["abort"] == "true":
                    response = Formatter.format(inference["message"],"")

                    

            #somethines even though parameters are collected still llm fails mark completed as true

            response["intent"] = request["intent_extractor"]["intent"]
            response["inference"] = {
                "params" : inference.get("params", {}),
                "abort" : inference.get("abort", "false"),
                "missing_params" : missing_params
                }
            response["summary"] = inference.get("summary", "")
            response["question"] = request["question"]
            response["context_id"] = request["context_id"]
        else:
            logger.info("No intents detected")
            response = Formatter.format("Sorry, I didn't get that","")

        return super().handle(response)

