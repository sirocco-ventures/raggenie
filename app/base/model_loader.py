class ModelLoader:


    def __init__(self, model_config):
        self.model_config = model_config

    def load_model(self):
        raise NotImplementedError("load_model method must be implemented in subclass")

    def get_response(self) -> dict:
        raise NotImplementedError("load_model method must be implemented in subclass")

    def get_usage(self, prompt, response, out) -> dict:
        raise NotImplementedError("load_model method must be implemented in subclass")

    def get_models(self):
        raise NotImplementedError("load_model method must be implemented in subclass")