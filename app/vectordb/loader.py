from app.vectordb.chromadb.handler import ChromaDataBase
from app.vectordb.mongodb.handler import AltasMongoDB

from loguru import logger



class VectorDBLoader:
    def __init__(self, config):
        self.config = config

    def load_class(self):
        vectordb_classes = {
            "chroma": ChromaDataBase,
            "mongodb": AltasMongoDB,
        }
        vectordb_provider = self.config.get('name',{})
        connection_params = self.config.get('params',{})


        vectordb_class = vectordb_classes.get(vectordb_provider)
        logger.info(f"vectordb provider: {vectordb_provider}")

        if vectordb_class:
            return vectordb_class(**connection_params)
        else:
            logger.info("No specified vectordb providers")
            return ChromaDataBase()