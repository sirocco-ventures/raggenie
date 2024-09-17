from app.base.abstract_handlers import AbstractHandler
from typing import Any, Optional
from loguru import logger
from app.providers.config import configs
from app.loaders.base_loader import BaseLoader
from string import Template
from app.utils.parser import parse_llm_response
import json


class MetadataGenerator(AbstractHandler):
    
    def __init__(self, common_context , model_configs) -> None:
        self.model_configs = model_configs
        self.common_context = common_context
        
    def handle(self, request: Any) -> str:
        response = request
        logger.info("passing through => Metadata description generator")
        rag = request["rag"]
        dbcontexts = rag["context"]

        contexts = ""
        for cont in dbcontexts:
            datasource_name = cont['metadatas']['datasource'].replace("_"," ")
            contexts += "Plugin Name: "+ datasource_name + "\n" + cont["document"] + "\n\n"

        prompt = """
            You are part of a chatbot system where you need to answer user questions based on the given database schema and context. 
            Please review the following information carefully:
            
            A brief description about the schema is given below:
            -- start db schema context section--
            $context
            -- end db schema context section--
            
            Make sure to follow these:
            1. Use the provided schema and context to inform your answer.
            2. while listing tables and its columns strictly mention under which plugin name it is.
            3. Provide accurate information based on the available data.
            4. If the question cannot be fully answered with the given information, explain what can be answered and what additional information might be needed.
            5. Keep the explanation concise but informative, focusing on how the schema and context led to your answer.
            6.Present the answer in a human-readable Markdown format, using appropriate Markdown syntax for headings, lists, emphasis, and other formatting as needed to enhance readability and structure.

            Your task is to go through the chat history carefully to understand the user's context and instructions. Then, generate a response to the user query '$question' using the provided schema and metadata information. Format your response in the following JSON structure:
            {
            "answer": '''Provide a clear, structured, and human-readable answer in Markdown format to the user's question using the available plugin name information''
            }      
        """

        prompt = Template(prompt).safe_substitute(question = request["question"], context =contexts)
        response["prompt"] = prompt
        
        logger.info(prompt)
        llm = self.common_context["llm"]
        llm["name"] = configs.inference_llm_model

        chat_history = []
        if "context" in request and len(request["context"]) > 0:
            chat_history = request["context"]
            chat_history = chat_history[-7:] if len(chat_history) >= 7 else chat_history

        loader = BaseLoader(model_configs=self.model_configs["models"])
        infernce_model = loader.load_model(configs.inference_llm_model)
                
        output, response_metadata = infernce_model.do_inference(
                            prompt, chat_history
                    )      
        parsed = parse_llm_response(output)

        response["inference"]  = parsed    
        response["summary"] = ""
        return super().handle(response)