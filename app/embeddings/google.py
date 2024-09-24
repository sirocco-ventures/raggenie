
import chromadb.utils.embedding_functions as embedding_functions
from loguru import logger


class Google:
    def __init__(self,model_name:str = "",api_key:str = ""):
        logger.info("Initialising embedding providers")
        self.ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=api_key)

    def load_emb(self):
        return self.ef
