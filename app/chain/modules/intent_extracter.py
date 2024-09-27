from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
from app.providers.config import configs
from app.loaders.base_loader import BaseLoader
from string import Template
from app.utils.parser import parse_llm_response


class IntentExtracter(AbstractHandler):
    """
    A handler for extracting user intents from chat queries based on a provided use case configuration.

    This class processes chat requests to determine the intent behind user queries using a language model.
    It generates a prompt with the chat context, available intents, and instructions to guide the model in
    intent extraction.

    Attributes:
        common_context (Any): Shared context information used across handlers.
        model_configs (dict): Configuration settings for the model, including use case details and model paths.
    """

    def __init__(self, common_context , model_configs) -> None:
        """
        Initializes the IntentExtractor with common context and model configurations.

        Args:
            common_context (Any): Shared context information used across handlers.
            model_configs (dict): Configuration settings for the model.
        """
        self.model_configs = model_configs
        self.common_context = common_context

    def handle(self, request: Any) -> str:
        """
        Processes the request to extract the intent from the user's query.

        Args:
            request (Any): The incoming request containing the user query and context.

        Returns:
            str: The result of the superclass's handle method with updated response information.
        """

        response = request
        logger.info("passing through => Intent extractor")

        use_case = self.model_configs.get("use_case", {})
        long_description = use_case.get("long_description", "")
        short_description = use_case.get("short_description", "")
        capabilities = use_case.get("capabilities", [])

        capability_description = ""
        capability_names = ["out_of_context", "metadata_inquiry"]

        for capability in capabilities:
            name = capability["name"]
            description = capability["description"]
            capability_names.append(name)
            capability_description += f"{name} : {description}\n"


        datasources = self.model_configs.get("datasources", [])
        datasource_names = []
        for datasource in datasources:
            name = datasource["name"]
            description = datasource["description"]
            capability_names.append(name)
            datasource_names.append(name)
            capability_description += f"{name} : {description}\n"
        response["available_datasources"] = datasource_names


        contexts = request.get("context", [])
        contexts = contexts[-5:] if len(contexts) >= 5 else contexts

        prompt = """
        You are part of a chatbot system where you have to extract intent from users chats and match it with given intents.

        -- chatbot context ---
        $long_description
        Also provide data structure information and overview of available data.
        -- chatbot context ---

        Available intents are:
        -- Intent section ---
        metadata_inquiry: queries about overview of available data, the structure of a database (including tables and columns), the meaning behind specific columns, and the purpose within a database context, eg: what kind of data you have? or list questions which can be asked?
        $capabilities
        out_of_context: If chat is irrelevant to chatbot context and its capabilities
        --- Intent section ---

        Instructions:
        1.Only one intent must be identified.Multiple intents are prohibited.
        2.Pay special attention to whether the previous intent has been completed.
        3.Strictly only if the current user query doesn't clearly match an intent, consider the previous messages to identify the most appropriate intent.
        3.If user seeks data structure info or data overview, label intent as metadata_inquiry.
        4.When asked to list possible questions, provide general examples without mentioning "specific" word

        Generate a response for the user query '$question' in the following JSON format:

        {
            "explanation": "Explain how you finalized the intent based on user context and instructions. Include your reasoning for determining whether the previous intent was completed or if the current query relates to a new intent.",
            "intent": "Detected intent, strictly one from the $capability_list"
        }
        """



        capability_list = "|".join(capability_names)

        prompt = Template(prompt).safe_substitute(
            question = request["question"],
            long_description = long_description,
            short_description =short_description,
            capability_list = capability_list,
            capabilities= capability_description
        )
        logger.debug(f"intent prompt:{prompt}")

        loader = BaseLoader(model_configs=self.model_configs["models"])
        infernce_model = loader.load_model(configs.inference_llm_model)

        output, response_metadata = infernce_model.do_inference(
                            prompt, contexts
                    )
        response["intent_extractor"] = {}
        if 'content' in output:
            response["intent_extractor"] = parse_llm_response(output['content'])

        response["available_intents"] = capability_names
        response["rag_filters"] = {
             "datasources" : [response["intent_extractor"]['intent']] if 'intent_extractor' in response else [],
             "document_count" : 5,
             "schema_count" : 5
        }
        return super().handle(response)


