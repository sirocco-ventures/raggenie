from .onnx import DefaultEmbeddingModel

from loguru import logger

class DefaultEmbedding:
    def __init__(self,model_name:str = "",api_key:str = ""):
        logger.info("Initialising embedding providers")
        self.ef = DefaultEmbeddingModel()

    def load_emb(self):
        return self.ef

