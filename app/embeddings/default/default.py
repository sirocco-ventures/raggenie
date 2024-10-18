from .onnx import DefaultEmbeddingModel

from loguru import logger

class DefaultEmbedding:
    def __init__(self):
        logger.info("Initialising embedding providers")
        self.ef = DefaultEmbeddingModel()

    def load_emb(self):
        return self.ef

    def health_check(self) -> None:
        pass

