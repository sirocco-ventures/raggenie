from app.base.abstract_handlers import AbstractHandler
from typing import Any, Optional
from app.providers.config import configs
from app.loaders.base_loader import BaseLoader
from app.utils.parser import parse_llm_response
from loguru import logger
import time
import math

class Generator(AbstractHandler):
        """
        A handler class for generating inferences based on prompts and contexts.

        This class extends AbstractHandler and provides functionality to generate
        inferences using a specified language model based on given prompts and contexts.
        """
    
        def __init__(self, common_context, model_configs) -> None:
                """
                Initialize the Generator.

                Args:
                common_context (Dict[str, Any]): The common context shared across handlers.
                model_configs (Dict[str, Any]): Configuration for the models used in processing.
                """
                self.model_configs = model_configs
                self.common_context = common_context
        
        def handle(self, request: dict) -> str:
                """
                Handle the incoming request by generating an inference based on the prompt and context.

                This method extracts the prompt and context from the request, uses an inference model
                to generate a response, and adds the parsed inference to the response.

                Args:
                request (Dict[str, Any]): The incoming request to be processed.

                Returns:
                str: The response after processing the request, including the generated inference.
                """
                logger.info("passing through => generator")
                
                response = request
                prompt = response["prompt"]

                contexts = request.get("context",[])
                contexts = contexts[-5:] if len(contexts) >= 5 else contexts

                loader = BaseLoader(model_configs=self.model_configs["models"])
                infernce_model = loader.load_model(configs.inference_llm_model)
                
                start_time = time.time()
                output, response_metadata = infernce_model.do_inference(
                        prompt, contexts
                )      
                
                latency = time.time() - start_time
                
                parsed = parse_llm_response(output)
                response["inference"]  = parsed
                
                return super().handle(response)
