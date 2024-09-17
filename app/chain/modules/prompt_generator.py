from app.base.abstract_handlers import AbstractHandler
from typing import Any, Optional
from loguru import logger
from string import Template
import json

class PromptGenerator(AbstractHandler):
    """
    A handler for generating prompts based on the provided context, model configurations, and data sources.

    This class creates a formatted prompt for the model by combining various elements such as system prompts,
    user prompts, and context information. It supports both manual and automatic prompt injection modes.

    Attributes:
        common_context (dict): Shared context information used across handlers.
        model_configs (dict): Configuration settings for the model, including prompt injection settings.
        data_sources (dict): Data sources for generating prompt contexts based on intent.
    """
    
    
    def __init__(self, common_context , model_configs, data_sources) -> None:
        """
        Initializes the PromptGenerator with common context, model configurations, and data sources.

        Args:
            common_context (dict): Shared context information used across handlers.
            model_configs (dict): Configuration settings for the model.
            data_sources (dict): Data sources for generating prompt contexts based on intent.
        """
        
        self.model_configs = model_configs
        self.common_context = common_context
        self.data_sources = data_sources
        
    def handle(self, request: Any) -> str:
        """
        Generates a prompt based on the incoming request and provided configurations.
        Args:
            request (Any): The incoming request containing data for prompt generation.

        Returns:
            str: The result of the superclass's handle method with the generated prompt included in the response.
        """
        
        logger.info("passing through => prompt_generator")
        response = request
        
        # Few shot prompting
        samples_retrieved = ""
        recal_history = ""
        
        rag = request.get("rag", {})
        suggestions = rag.get("suggestions", [])

        for doc in suggestions:
            samples_retrieved += f"question: {doc.get('document', '')}\n"
            samples_retrieved += f"query: {doc.get('metadatas', {}).get('query', '')}\n\n"
        
        
        prompt_injection = self.model_configs.get("prompt_injection", {"mode": "auto"})
        data_source = self.data_sources.get(self.common_context.get("intent", "default"))
        
        context = data_source.__prompt__
        prompt = context.base_prompt
        
        
        system_prompt = ""
        
        if prompt_injection["mode"] == "manual" :
            system_prompt_context = context.system_prompt
            system_prompt = system_prompt_context.template.format(
                **{**system_prompt_context["prompt_variables"]}
            )    
        else:
            auto_context = "\n\n".join(cont["document"] for cont in rag.get("context", []))
            auto_schema = "\n\n".join(schema["document"] for schema in rag.get("schema", []))
            system_prompt_context = context.system_prompt
            system_prompt= system_prompt_context.template.format(
                schema=auto_schema,
                context=auto_context,
                question=request.get("question", ""),
                suggestions="",
                recall=recal_history
            )
        

        user_prompt = ""
            
        if self.common_context["chain_retries"] == 0:
            user_prompt = context.user_prompt.template
        else:
            logger.info("regenerating prompt using avaialable context")
            regeneration_promt_context = context.regeneration_prompt
            
            user_prompt = Template(regeneration_promt_context.template).safe_substitute(
                exception_log =self.common_context["execution_logs"][0]["error"] if len(self.common_context["execution_logs"])>0 else "",
                query_generated =self.common_context["execution_logs"][0]["query"] if len(self.common_context["execution_logs"])>0 else ""
            )
                    
        final_prompt = prompt.format(user_prompt=user_prompt, system_prompt=system_prompt)
        final_prompt = Template(final_prompt).safe_substitute(
            question=request.get("question", ""),
            suggestions=samples_retrieved,
            **self.model_configs.get("use_case", {})
        )
        
        response["prompt"] = final_prompt
        return super().handle(response)
