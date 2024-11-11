from app.chain.modules.input_formatter import InputFormatter
# from app.chain.modules.guard_rail import GuardRail
from app.chain.modules.rag_module import RagModule
from app.chain.modules.prompt_generator import PromptGenerator
from app.chain.modules.general_answer_generator import GeneralAnswerGenerator
from app.chain.modules.ouput_formatter import OutputFormatter
from app.chain.modules.post_processor import PostProcessor

from app.chain.modules.context_retreiver import ContextRetreiver




from loguru import logger

class GeneralChain:
    """
    Chain class represents the main processing chain for handling user requests.

    This class orchestrates various modules to process user input, retrieve context,
    generate prompts, execute actions, and format output.

    Attributes:
        vector_store: A storage system for vector embeddings.
        data_sources: A list of data sources to be used in processing.
        context_store: A storage system for maintaining context across interactions.
        common_context (dict): A shared context dictionary used across modules.
        configs (dict): Configuration settings for the models.
        input_formatter (InputFormatter): Module for formatting user input.
        rag_module (RagModule): Module for Retrieval-Augmented Generation.
        prompt_generator (PromptGenerator): Module for generating prompts.
        generator (Generator): Module for generating responses.
        validator (Validator): Module for validating responses.
        context_retriver (ContextRetreiver): Module for retrieving context.
        context_storage (ContextStorage): Module for storing context.
        executer (Executer): Module for executing actions.
        cache_checker (Cachechecker): Module for checking and managing cache.
        output_formatter (OutputFormatter): Module for formatting output.

    The Chain class follows a modular design, where each module is responsible
    for a specific part of the processing pipeline. This allows for flexibility
    and easy extension of functionality.
    """
    def __init__(self, model_configs, store, datasource, context_store):

        logger.info("loading modules into chain")


        self.vector_store = store
        self.data_sources = datasource if datasource is not None else []
        self.context_store = context_store

        self.common_context = {
            "chain_retries" : 0,
            "rag": {
                "context": [],
                "schema" : [],
            },
        }

        self.configs = model_configs
        self.input_formatter = InputFormatter()
        self.rag_module = RagModule(model_configs, self.vector_store, self.common_context)
        self.prompt_generator = PromptGenerator(self.common_context, model_configs, self.data_sources)
        self.generator = GeneralAnswerGenerator(self.common_context, model_configs)
        self.context_retriver = ContextRetreiver(self.common_context, context_store)
        self.output_formatter = OutputFormatter(self.common_context,self.data_sources)

        self.post_processor = PostProcessor()

        logger.info("initializing chain")

        self.input_formatter.set_next(self.rag_module) \
        .set_next(self.context_retriver) \
        .set_next(self.prompt_generator).set_next(self.generator).set_next(self.output_formatter).set_next(self.post_processor)

        self.handler =  self.input_formatter


    def invoke(self, user_request):
        self.common_context["chain_retries"] = 0
        self.common_context["intent"] = user_request["intent_extractor"]["intent"]
        self.common_context["context_id"] = user_request["context_id"]
        self.common_context["rag"].update({
            "context": [],
            "schema" : [],
        })
        return self.handler.handle(user_request)
