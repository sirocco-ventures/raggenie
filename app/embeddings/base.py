import chromadb.utils.embedding_functions as embedding_functions
from loguru import logger

class Base:
    def __init__(self,model_name:str = "",api_key:str = ""):
        logger.info("Initialising embedding providers")
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)

    def load_emb(self):
        return self.ef
    




    