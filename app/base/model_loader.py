from loguru import logger
import json

class ModelLoader:


    def __init__(self, model_config):
        self.model_config = model_config

    def load_model(self):
        raise NotImplementedError("load_model method must be implemented in subclass")

    def get_response(self) -> dict:
        raise NotImplementedError("load_model method must be implemented in subclass")

    def get_usage(self, prompt, response, out) -> dict:
        raise NotImplementedError("load_model method must be implemented in subclass")
    
   
    def messages_format(self, prompt, previous_messages) -> list:
        chat_history = []
        for prev_message in previous_messages:
            chat_history.append({"role": "user", "content": prev_message.chat_query})
            if prev_message.chat_answer is not None:
                answer = self.chat_answer_format(prev_message.chat_answer)
                chat_history.append({"role": "assistant", "content": json.dumps(answer)})
        messages = []
        if len(chat_history) > 0:
            messages.extend(chat_history)
        messages.append({"role": "user", "content": prompt})
        logger.info(f"messages:{messages}")
        return messages
    
    def chat_answer_format(self, response: dict) -> dict:
        answer = {}
        if response['main_format'] == 'query_chat':
            if len(response['data']) > 0:
                answer["general_message"] = response['content']
                answer["intent"] = response.get("intent","")
                # answer['data'] = response['data'][-12:] if len(response['data']) > 12 else response['data']
                answer["metadata"] = f"There were {len(response['data'])} data entries available"
            else:
                answer["general_message"] = response['empty_message']
        else:
            answer["general_message"] = response['content']

        logger.info(f"answer:{answer}")
        return answer
