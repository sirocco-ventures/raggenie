from app.base.abstract_handlers import AbstractHandler
from typing import Any, Optional
from loguru import logger
from app.providers.container import Container
from app.providers.config import configs
from app.chain.chains.rag_chain import RAGChain



class RagModule(AbstractHandler):
    """
    A handler for managing RAG (retrieval-augmented generation) processing based on model configurations.

    This class integrates with the RAGChain to perform retrieval-augmented generation if the prompt injection mode
    is not set to 'manual'. It processes the incoming request, applies RAG filters, and updates the response with
    the results from the RAGChain.

    Attributes:
        store (object): Data store for RAG processing.
        configs (dict): Model configurations, including prompt injection settings.
        common_context (dict): Shared context information used across handlers.
    """
    
    def __init__(self, model_configs, store, common_context):
        """
        Initializes the RagModule with model configurations, data store, and common context.

        Args:
            model_configs (dict): Configuration settings for the model, including prompt injection mode.
            store (object): Data store for RAG processing.
            common_context (dict): Shared context information used across handlers.
        """
        self.store = store
        self.configs = model_configs
        self.common_context = common_context

    def handle(self, request: Any) -> str:
        """
        Processes the request using RAGChain if prompt injection mode is not 'manual'.

        Args:
            request (Any): The incoming request containing question, filters, and intent extractor.

        Returns:
            str: The result of the superclass's handle method with updated response information.
        """
        logger.info("passing through => rag_module")
        
        response = request
        
        prompt_injection = self.configs.get("prompt_injection", {"mode": "auto"})
        if prompt_injection["mode"] != "manual" :   
            response = request
            question = request.get("question", "")
            rag_filters = response.get("rag_filters", {})
            intent_extractor = request.get("intent_extractor", {})
            
            rag_chain = RAGChain(self.configs, self.store)
            out = rag_chain.invoke({
                "question": question,
                "rag_filters": rag_filters,
                "intent_extractor": intent_extractor,
            })

            if out is None:
                gen_formatter = self.common_context["general_response"]
                return gen_formatter.format("Sorry, It is out of my context to answer!")

            if 'rag' in response:
                response["rag"].update(out["rag"])
            else:
                response = out
        else:
            logger.info("skipped rag module for manual mode")

        return super().handle(response)

