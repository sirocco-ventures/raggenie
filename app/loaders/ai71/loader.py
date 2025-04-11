from app.base.model_loader import ModelLoader
from app.base.loader_metadata_mixin import LoaderMetadataMixin
from app.base.base_llm import BaseLLM
from typing import Any
import json
import requests

class Ai71ModelLoader(ModelLoader, LoaderMetadataMixin):

    model: Any = None
    model_config : Any = {}

    def do_inference(self, prompt, previous_messages) -> dict:
        messages = self.messages_format(prompt, previous_messages)

        self.model = BaseLLM(
            url = self.model_config["endpoint"],
            headers = {
                "Authorization": "Bearer "+self.model_config["api_key"],
            },
            body = {
                "temperature" : 0.5,
                "model": self.model_config["name"],
                "messages": messages
            }
        )

        out = self.model._call("")

        response = self.get_response(out)
        usage = self.get_response_metadata(prompt, response, out)

        return response, usage

    def get_response(self, message) -> dict:
        if "choices" in message and len(message["choices"]) > 0:
            choice = message["choices"][0]
            if "message" in choice:
                return {"content" : choice["message"]["content"], "error" : None}
        elif "error" in message:
            error = message["error"]
            if "message" in error:
                return {"content" : "", "error" : error["message"]}
        elif "detail" in message:
            return {"content" : "", "error" : message["detail"]}
        return {"content" : "", "error" : "Empty Response from LLM Provider"}

    def get_response_metadata(self, prompt, response, out) -> dict:

        return{
                "input_tokens" : 0,
                "output_tokens" : 0,
                "logprobs" : [],

        }

    def get_models(self):

        """
        Retrieve models from the AI71 API and reformat the response.
        Args:
            llm_provider: The LLM provider object with API key.
        Returns:
            List of reformatted model information or an error message.
        """
        url = "https://api.ai71.ai/v1/models"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                models = [{"display_name": model["name"], "id": model["id"]} for model in data.get("data", [])]
                return models, False
            else:
                return f"Failed to retrieve AI71 models: {response.status_code} {response.text}", True
        except requests.RequestException as e:
            return f"Error occurred: {str(e)}", True
