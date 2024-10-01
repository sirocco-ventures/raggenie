from app.chain.modules.input_formatter import InputFormatter

from app.chain.modules.intent_extracter import IntentExtracter
from app.chain.modules.router import Router
from app.chain.modules.post_processor import PostProcessor
from app.chain.formatter.general_response import Formatter
from app.chain.modules.context_retreiver import ContextRetreiver


from loguru import logger

class IntentChain:
    """
    IntentChain class represents the main processing chain for handling user intents.

    This class orchestrates various modules to process user input, extract intents,
    route requests, and manage context across interactions.

    Attributes:
        vector_store: A storage system for vector embeddings.
        data_source: A data source to be used in processing.
        context_store: A storage system for maintaining context across interactions.
        common_context (dict): A shared context dictionary used across modules.
        configs (dict): Configuration settings for the models.
        input_formatter (InputFormatter): Module for formatting user input.
        context_retriver (ContextRetreiver): Module for retrieving context.
        intent_extractor (IntentExtracter): Module for extracting intents from user input.
        post_processor (PostProcessor): Module for post-processing responses.
        router (Router): Module for routing requests to appropriate chains.
        handler: The first module in the processing chain.

    The IntentChain class follows a modular design, where each module is responsible
    for a specific part of the processing pipeline. This allows for flexibility
    and easy extension of functionality.
    """
    def __init__(self, model_configs, store, datasource, context_store, intent_chain, general_chain, capability_chain, metadata_chain):
        logger.info("loading modules into chain")

        self.vector_store = store
        self.context_store = context_store
        self.data_sources = datasource if datasource is not None else []

        self.common_context = {
            "chain_retries" : 0,
        }

        self.configs = model_configs
        self.input_formatter = InputFormatter()
        self.context_retriver = ContextRetreiver(self.common_context, context_store)
        self.intent_extractor = IntentExtracter(self.common_context, model_configs)
        self.post_processor = PostProcessor()
        self.router = Router(self.common_context, self.post_processor, intent_chain, general_chain, capability_chain, metadata_chain)

        self.input_formatter.set_next(self.context_retriver).set_next(self.intent_extractor).set_next(self.router).set_next(self.post_processor)

        self.handler =  self.input_formatter


    def invoke(self, user_request):
        try:
            self.common_context["chain_retries"] = 0
            self.common_context["context_id"] = user_request["context_id"]
            return self.handler.handle(user_request)
        except Exception as error:
            logger.error(f"An error occurred: {error}")
            return Formatter.format("Oops! Something went wrong. Try Again!",error)
