from app.embeddings.cohere import Cohere
from app.embeddings.google import Google
from app.embeddings.base import Base
from app.embeddings.default import DefaultEmbedding
from app.embeddings.chroma_default import ChromaDefaultEmbedding


from loguru import logger





class EmLoader:
    def __init__(self, configs):
        self.config = configs

    def load_embclass(self):
        emb_classes = {
            "google": Google,
            "cohere" : Cohere,
            "base": Base,
            "chroma_default": ChromaDefaultEmbedding,
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