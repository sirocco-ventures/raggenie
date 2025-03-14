from app.base.model_loader import ModelLoader
from app.base.base_llm import BaseLLM
from typing import Any
from loguru import logger
from app.base.loader_metadata_mixin import LoaderMetadataMixin
import json
import requests


class OllamaModelLoader(ModelLoader, LoaderMetadataMixin):

    model: Any = None
    model_config : Any = {}

    def do_inference(self, prompt, previous_messages) -> dict:
        messages = self.messages_format(prompt, previous_messages)
        self.model = BaseLLM(
            url = self.model_config["endpoint"],
            body = {
                "model": self.model_config["name"],
                "messages": messages,
                "stream" : False
            }
        )

        out = self.model._call("")
        logger.info(f"response:{out}")
        response = self.get_response(out)
        usage = self.get_response_metadata(prompt, response, out)

        return response, usage

    def get_response(self, message) -> dict:
        if "message" in message:
            message = message["message"]
            if "content" in message:
                return {"content" : message["content"], "error" : None}
        elif "error" in message:
            error = message["error"]
            return {"content" : "", "error" : error}
        return {"content" : "", "error" : "Empty Response from LLM Provider"}

    def get_response_metadata(self, prompt, response, out) -> dict:
        response_metadata = {}
        if "usage" in out:
            usage = out["usage"]
            response_metadata.update({
                "input_tokens" : usage["prompt_tokens"],
                "output_tokens" : usage["completion_tokens"],
            })
        else:
            response_metadata.update({
                "input_tokens" : len(prompt),
                "output_tokens" : len(out),
            })
        if "choices" in out and len(out["choices"]) > 0:
            choice = out["choices"][0]
            if "logprobs" in choice and choice["message"]["content"] != '' and choice['logprobs'] is not None:
                response_metadata.update({
                                    "logprobs" : [logprob['logprob'] for logprob in choice['logprobs']['content']]
                                })

                return response_metadata


        response_metadata.update({
                "logprobs" : []
            })
        return response_metadata

    def messages_format(self, prompt, previous_messages) -> list:
        chat_history = []
        for prev_message in previous_messages:
            chat_history.append({"role": "user", "content": prev_message.chat_query})
            if prev_message.chat_answer is not None:
                temp = prev_message.chat_answer
                temp.pop("data", None)
                chat_history.append({"role": "assistant", "content": json.dumps(temp)})

        messages = []
        if len(chat_history) > 0:
            messages.extend(chat_history)
        messages.append({"role": "user", "content": prompt})

        logger.info(f"messages:{messages}")
        return messages

    def get_models(self):
            """
            Retrieve models from the Ollama API.
            Returns:
                List of Ollama model names or an error message.
            """
            url = "curl http://localhost:11434/api/tags"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    models = [{"display_name": model["id"], "id": model["id"]} for model in data.get("data", [])]
                    return models, False
                else:
                    return f"Failed to retrieve Ollama models: {response.status_code} {response.text}", True
            except requests.RequestException as e:
                return f"Error occurred: {str(e)}", True