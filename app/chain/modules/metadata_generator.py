from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
from app.providers.config import configs
from app.loaders.base_loader import BaseLoader
from string import Template
from app.utils.parser import markdown_parse_llm_response
from app.chain.formatter.general_response import Formatter



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
            datasource_name = cont['metadata'].get('datasource','').replace("_"," ")
            contexts += "Plugin/Database Name: "+ datasource_name + "\n" + cont["document"] + "\n\n"

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
            4. Keep the answer concise and with minimal explanation
            5. If the question cannot be fully answered with the given information, explain what can be answered and what additional information might be needed.
            6. Present the answer in a human-readable Markdown format
            7. Give only what user wants, don't hallucinate to give long answers

            Your task is to go through the chat history carefully to understand the user's context and instructions. Then, generate a response to the user query '$question' using the provided schema and metadata information. Format your response in the following JSON structure:
            {
            "general_message": "Provide a concise human-readable answer in Markdown format to the user's question using the available information",
            }
        """

        prompt = Template(prompt).safe_substitute(question = request["question"], context =contexts)
        response["prompt"] = prompt

        chat_history = []
        if "context" in request and len(request["context"]) > 0:
            chat_history = request["context"]
            chat_history = chat_history[-7:] if len(chat_history) >= 7 else chat_history

        loader = BaseLoader(model_configs=self.model_configs["models"])
        infernce_model = loader.load_model(configs.inference_llm_model)

        output, response_metadata = infernce_model.do_inference(
                            prompt, chat_history
                    )
        if output["error"] is not None:
            return Formatter.format("Oops! Something went wrong. Try Again!",output['error'])

        response["inference"] = markdown_parse_llm_response(output['content'])

        response["summary"] = ""
        return super().handle(response)