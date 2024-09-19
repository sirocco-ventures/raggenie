
from app.loaders.togethor.loader import TogethorModelLoader
from app.loaders.openai.loader import OpenAiModelLoader
from app.loaders.ai71.loader import Ai71ModelLoader



class BaseLoader:
    def __init__(self, model_configs):
        self.model_configs = model_configs

    def load_model(self, unique_name):
        for model in self.model_configs:
            if model['unique_name'] == unique_name:
                match model['kind']:
                    case "togethor":
                        loader = TogethorModelLoader(model_config=model)
                    case "openai":
                        loader = OpenAiModelLoader(model_config = model)
                    case "ai71":
                        loader = Ai71ModelLoader(model_config = model)
                    case _ :
                        raise ValueError(f"Model with unique name '{unique_name}' not found.")
                return loader

        raise ValueError(f"Model with unique name '{unique_name}' not found.")

    def load_model_config(self, unique_name):
        for model in self.model_configs:
            if model['unique_name'] == unique_name:
                return model
