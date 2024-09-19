from app.base.abstract_handlers import AbstractHandler
from loguru import logger
from typing import Any
from app.providers.container import Container


class DocumentRetriever(AbstractHandler):
    """
    A handler class for retrieving relevant documents based on the input question.

    This class extends AbstractHandler and provides functionality to find and
    process similar documents from a vector store based on the input question.
    """

    def __init__(self,store):
        """
        Initialize the DocumentRetriever.

        Args:
            store (Any): The vector store for document retrieval.
        """

        self.store =store
        self.context_relevance_threshold = 4


    def handle(self, request: Any) -> str:
        """
        Handle the incoming request by retrieving relevant documents.

        Args:
            request (Dict[str, Any]): The incoming request to be processed.

        Returns:
            str: The response after processing the request.
        """

        logger.info("passing through => document_retriever")
        response = request
        datasources = request['rag_filters']["datasources"]
        document_count = request['rag_filters']["document_count"]
        intent = request["intent_extractor"]["intent"]
        out = self.store.find_similar_documentation(datasources, request["question"], document_count)



        logger.info("sorting retrieved documents")
        if out and len(out) > 0 and out[0]['distances'] < self.context_relevance_threshold:

            distances = [doc['distances'] for doc in out]
            if len(out) > 2 and intent != 'metadata_inquiry':
                clusters = Container.clustering().kmeans(distances, 2)
                shortest_cluster = clusters[0]
                opt_doc = []
                for doc in out:
                    if doc['distances'] in shortest_cluster:
                        opt_doc.append(doc)
            else:
                opt_doc = out

            response["rag"]={
                "context": opt_doc,
            }
        else:
            response["rag"]={
                "context": [],
            }

        return super().handle(response)





