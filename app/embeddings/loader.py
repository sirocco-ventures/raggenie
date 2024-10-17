from app.embeddings.google. handler import GoogleEm
from app.embeddings.default.default import DefaultEmbedding
from app.embeddings.openai.handler import OpenAIEm
from app.embeddings.cohere.handler import CohereEm


from loguru import logger





class EmLoader:
    def __init__(self, configs):
        self.config = configs

    def load_embclass(self):
        emb_classes = {
            "google": GoogleEm,
            "openai": OpenAIEm,
            "cohere": CohereEm,
            "default": DefaultEmbedding,

        }
        emb_provider = self.config.get("provider")
        connection_params = self.config.get("params")


        emb_class = emb_classes.get(emb_provider)
        logger.info(f"embedding class: {emb_provider}")
        if emb_class:
            return emb_class(**connection_params if connection_params else {})
        else:
            logger.info("No specified embedding providers")
            return DefaultEmbedding()