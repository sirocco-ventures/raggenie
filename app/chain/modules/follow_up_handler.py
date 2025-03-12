from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
from app.providers.config import configs
from app.loaders.base_loader import BaseLoader
from string import Template
from app.utils.parser import parse_llm_response
from app.chain.formatter.general_response import Formatter

class FollowupHandler(AbstractHandler):
    """
    A handler class for processing follow-up queries and extracting required parameters.

    This class extends AbstractHandler and provides functionality to process
    follow-up queries, extract intent-specific parameters, and generate appropriate responses.
    """

    def __init__(self, common_context , model_configs) -> None:
        """
        Initialize the FollowupHandler.

        Args:
            common_context (Dict[str, Any]): The common context shared across handlers.
            model_configs (Dict[str, Any]): Configuration for the models used in processing.
        """

        self.model_configs = model_configs
        self.common_context = common_context

    async def handle(self, request: Any) -> str:
        """
        Handle the incoming request by processing follow-up queries and extracting parameters.

        Args:
            request (Dict[str, Any]): The incoming request to be processed.

        Returns:
            str: The response after processing the request.
        """
        response = request
        logger.info("passing through => Intent extractor")

        use_case = self.model_configs.get("use_case", {})
        capabilities = use_case.get("capabilities", [])

        intent_extracted = request.get("intent_extractor")
        intent = intent_extracted.get("intent", "")

        filtered_capabilities = [capability for capability in capabilities if capability["name"]== intent]
        capability = filtered_capabilities[0]


        long_description = use_case["long_description"]
        capability_description = capability["description"]
        parameter_description = ""

        parameters = capability["requirements"]
        for parameter in parameters:
            parameter_description= parameter_description + parameter["parameter_name"]+ " : "+ parameter["parameter_description"]+"\n"

        prompt = """
                You are part of a Form automations system where your duty is to: $capability_description
                You will be given inputs that need to be captured. Your task is to ask and capture this information from the user and get it confirmed.

                -- Form system context ---
                $long_description
                -- Form system context ---

                Required parameters
                -- Parameter section ---
                $parameter_description
                --- Parameter section ---

                Instructions:
                Carefully review all previous messages to establish context.
                Only extract values that are explicitly provided in previous messages.
                Do not assume or fill in any values that are not present in previous messages.
                Do not hallucinate or claim that required values are present when they are not.

                Generate a JSON response in the following format for the query '$question':
                {
                  "explanation": "Describe which required values were found in previous messages and how they were extracted. If no values were found, state this clearly.",
                  "params": {},dont extract values for the params which is not mentioned in previous messages
                  "completed": "true|false, if all the required values are captured",
                  "message": "Ask for specific required parameters that have not been provided yet. If all parameters are captured, provide a success message for the booking.",
                  "summary" : "summarise question and answer in one sentence"
                }
          """

        contexts = request.get("context", [])
        contexts = contexts[-5:] if len(contexts) >= 5 else contexts

        prompt = Template(prompt).safe_substitute(
            question = request["question"],
            long_description= long_description,
            capability_description= capability_description,
            parameter_description=parameter_description
        )


        loader = BaseLoader(model_configs=self.model_configs["models"])
        infernce_model = loader.load_model(configs.inference_llm_model)

        output, response_metadata = infernce_model.do_inference(
                            prompt, contexts
                    )
        
        if output["error"] is not None:
            return await Formatter.format("Oops! Something went wrong. Try Again!",output['error'])

        response["inference"] = parse_llm_response(output['content'])
        response["capability"] = capability
        return await super().handle(response)


