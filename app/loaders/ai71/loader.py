from app.base.model_loader import ModelLoader
from app.base.loader_metadata_mixin import LoaderMetadataMixin
from app.base.base_llm import BaseLLM
from typing import Any
import json

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
                return choice["message"]
        elif 'detail' in message:
            return {"error" : message['detail']}
        return {"content" : ""}

    def get_response_metadata(self, prompt, response, out) -> dict:

        return{
                "input_tokens" : 0,
                "output_tokens" : 0,
                "logprobs" : [],

        }

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

        return messages