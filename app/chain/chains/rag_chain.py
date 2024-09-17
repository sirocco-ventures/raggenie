
from app.chain.modules.document_retriever import DocumentRetriever
from app.chain.modules.schema_retriever import SchemaRetriever


from loguru import logger

class RAGChain:
    """
    RAGChain class represents the Retrieval-Augmented Generation (RAG) chain for processing user requests.

    This class orchestrates the retrieval of relevant documents and schemas based on the user's query,
    enhancing the context for subsequent processing steps.

    Attributes:
        configs (dict): Configuration settings for the RAG chain.
        store: The vector store used for document and schema retrieval.
        document_retriever (DocumentRetriever): Module for retrieving relevant documents.
        schema_retriever (SchemaRetriever): Module for retrieving relevant schemas.
        handler: The first module in the processing chain.

    The RAGChain class implements the QueryPlugin interface and includes PluginMetadataMixin
    for metadata management. It follows a modular design where each retriever is responsible
    for a specific part of the information retrieval process.
    """

    
    def __init__(self,configs,store):
        logger.info("loading modules into RAG chain")
        self.configs = configs
        self.store = store

        self.document_retriever = DocumentRetriever(self.store)
        self.schema_retriever = SchemaRetriever(self.store)
        
        self.document_retriever.set_next(self.schema_retriever)
        self.handler =  self.document_retriever



    def invoke(self, user_request):
        
        return self.handler.handle(user_request)
