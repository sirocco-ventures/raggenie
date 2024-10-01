class ModelLoader:


    def __init__(self, model_config):
        self.model_config = model_config

    def load_model(self):
        raise NotImplementedError("load_model method must be implemented in subclass")

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

    def get_usage(self, prompt, response, out) -> dict:
        raise NotImplementedError("load_model method must be implemented in subclass")