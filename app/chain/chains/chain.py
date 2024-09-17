from app.chain.modules.input_formatter import InputFormatter
# from app.chain.modules.guard_rail import GuardRail
from app.chain.modules.rag_module import RagModule
from app.chain.modules.prompt_generator import PromptGenerator
from app.chain.modules.generator import Generator
from app.chain.modules.validator import Validator
from app.chain.modules.executer import Executer
from app.chain.modules.ouput_formatter import OutputFormatter
from app.chain.modules.post_processor import PostProcessor
from app.chain.formatter.general_response import Formatter
from app.chain.modules.cache_checker import Cachechecker

from app.chain.modules.context_retreiver import ContextRetreiver
from app.chain.modules.context_storage import ContextStorage

from app.providers.config import configs



from loguru import logger

class Chain:
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
            "llm": {
                "input_tokens" : 0,
                "output_tokens": 0,
                "total_cost": 0,
                "latency": 0,
                "response": {
                    "input_tokens" : 0,
                    "output_tokens": 0,
                    "total_cost": 0,
                    "latency": 0,
                    "logprob_percentage": 0,
                    "name": "default"
                    },
            },
            "execution_logs": [],
            "general_response": Formatter,
            "prompt_mode" : "manual",
            "inference_raw" : "",
            "prompt": "",
            "rag": {
                "context": [],
                "schema" : [],
            },
        }
        
        self.configs = model_configs
        self.input_formatter = InputFormatter()
        self.rag_module = RagModule(model_configs, self.vector_store, self.common_context)
        self.prompt_generator = PromptGenerator(self.common_context, model_configs, self.data_sources)
        self.generator = Generator(self.common_context, model_configs)
        self.validator = Validator(self.common_context,self.data_sources)
        self.context_retriver = ContextRetreiver(self.common_context, context_store)
        self.context_storage = ContextStorage(self.common_context, context_store)

       

        self.executer = Executer(self.common_context,self.data_sources, self.prompt_generator)
        self.cache_checker = Cachechecker(self.common_context, self.vector_store,self.executer)
        self.output_formatter = OutputFormatter(self.common_context,self.data_sources)
        self.post_processor = PostProcessor()

        logger.info("initializing chain")
        # self.input_formatter.set_next(self.guard_rail).set_next(self.rag_module)

        self.input_formatter.set_next(self.cache_checker).set_next(self.rag_module) \
        .set_next(self.context_retriver) \
        .set_next(self.prompt_generator).set_next(self.generator).set_next(self.validator).set_next(self.executer) \
        .set_next(self.output_formatter).set_next(self.post_processor)

        self.handler =  self.input_formatter
        
        
    def invoke(self, user_request):
        self.common_context["chain_retries"] = 0
        self.common_context["intent"] = user_request["intent_extractor"]["intent"]
        self.common_context["context_id"] = user_request["context_id"]
        self.common_context["llm"].update({
            "input_tokens" : 0,
            "output_tokens": 0,
            "total_cost": 0,
            "latency": 0,
            "response": {
                "input_tokens" : 0,
                "output_tokens": 0,
                "total_cost": 0,
                "latency": 0,
                "logprob_percentage": 0,
                "name": "default"
                },
        })
        self.common_context["prompt_mode"] = "manual"
        self.common_context["rag"].update({
            "context": [],
            "schema" : [],
        })
        return self.handler.handle(user_request)
