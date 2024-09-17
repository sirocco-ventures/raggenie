from app.chain.modules.input_formatter import InputFormatter
from app.chain.modules.post_processor import PostProcessor
from app.chain.modules.metadata_generator import MetadataGenerator
from app.chain.modules.context_retreiver import ContextRetreiver
from app.chain.modules.ouput_formatter import OutputFormatter
from app.chain.modules.metadata_ragfilter import MetadataRagFilter
from app.chain.modules.document_retriever import DocumentRetriever

from loguru import logger

class MetadataChain:
    """
    MetadataChain class represents the processing chain for handling metadata-related requests.

    This class orchestrates various modules to process user input, retrieve context,
    generate metadata, and format output for metadata-related operations.

    Attributes:
        vector_store: A storage system for vector embeddings.
        data_sources: A list of data sources to be used in processing.
        context_store: A storage system for maintaining context across interactions.
        common_context (dict): A shared context dictionary used across modules.
        input_formatter (InputFormatter): Module for formatting user input.
        context_retriver (ContextRetreiver): Module for retrieving context.
        document_retriever (DocumentRetriever): Module for retrieving relevant documents.
        metadata_generator (MetadataGenerator): Module for generating metadata.
        post_processor (PostProcessor): Module for post-processing responses.
        metadata_ragfilter (MetadataRagFilter): Module for filtering metadata using RAG.
        output_formatter (OutputFormatter): Module for formatting output.
        handler: The first module in the processing chain.

    The MetadataChain class follows a modular design, where each module is responsible
    for a specific part of the processing pipeline. This allows for flexibility
    and easy extension of functionality in metadata processing and generation.
    """
    def __init__(self, model_configs, store, datasource, context_store):
        logger.info("loading modules into metadata chain")
        self.vector_store = store
        self.data_sources = datasource if datasource is not None else []
        self.context_store = context_store
        
        self.common_context = {
            "chain_retries" : 0,
        }
        
        self.input_formatter = InputFormatter()
        self.context_retriver = ContextRetreiver(self.common_context, context_store)
        self.document_retriever = DocumentRetriever(self.vector_store)

        self.metadata_generator = MetadataGenerator(self.common_context, model_configs)
        self.post_processor = PostProcessor()
        self.metadata_ragfilter = MetadataRagFilter()
        self.output_formatter = OutputFormatter(self.common_context,self.data_sources)

        self.input_formatter.set_next(self.context_retriver).set_next(self.metadata_ragfilter).set_next(self.document_retriever).set_next(self.metadata_generator).set_next(self.output_formatter).set_next(self.post_processor)
        self.handler =  self.input_formatter
        
        
    def invoke(self, user_request):
        
        self.common_context["chain_retries"] = 0
        return self.handler.handle(user_request)
