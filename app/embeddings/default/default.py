from .onnx import DefaultEmbeddingModel
from .chroma_default import ChromaDefaultEmbedding

from loguru import logger
class DefaultEmbedding:
    def __init__(self, vectordb_key: str = "chroma"):
        logger.info("Initializing embedding providers")
        self.vectordb = vectordb_key

    def load_emb(self):
        match self.vectordb:
            case "chroma":
                print("================>>>, here")
                return ChromaDefaultEmbedding()
            case "mongodb":
                return DefaultEmbeddingModel()
            case _:
                logger.error(f"Unsupported vectordb_key: {self.key}")
                return None

    def health_check(self) -> None:
        pass
