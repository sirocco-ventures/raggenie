from app.base.model_loader import ModelLoader
from app.base.base_llm import BaseLLM
from typing import Any
from loguru import logger
from app.base.loader_metadata_mixin import LoaderMetadataMixin
import json

class TogethorModelLoader(ModelLoader, LoaderMetadataMixin):

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
                "messages": messages,
                "logprobs": 1,
            }
        )
        out = self.model._call("")
        logger.debug(out)
        response = self.get_response(out)
        respone_metadata = self.get_response_metadata(prompt, response, out)

        return response, respone_metadata

    def get_response(self, message) -> dict:
        if "choices" in message and len(message["choices"]) > 0:
            choice = message["choices"][0]
            if "message" in choice:
                return choice["message"]
        elif "error" in message:
            error = message["error"]
            if "message" in error:
                return {"error" : error["message"]}
        return {"content" : ""}

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
            if "message" in choice:
                if "logprobs" in choice and choice["message"]["content"] != '':
                    response_metadata.update({
                                        "logprobs" : choice['logprobs']['token_logprobs']
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