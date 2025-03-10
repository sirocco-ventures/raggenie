from app.base.abstract_handlers import AbstractHandler
from loguru import logger
from typing import Any
from app.providers.container import Container
import asyncio



class DocumentRetriever(AbstractHandler):
    """
    A handler class for retrieving relevant documents based on the input question.

    This class extends AbstractHandler and provides functionality to find and
    process similar documents from a vector store based on the input question.
    """

    def __init__(self,store, datasources):
        """
        Initialize the DocumentRetriever.

        Args:
            store (Any): The vector store for document retrieval.
        """

        self.store =store
        self.context_relevance_threshold = 4
        self.datasources = datasources


    async def handle(self, request: Any) -> str:
        """
        Handle the incoming request by retrieving relevant documents.

        Args:
            request (Dict[str, Any]): The incoming request to be processed.

        Returns:
            str: The response after processing the request.
        """

        logger.info("passing through => document_retriever")
        response = request
        tasks = [
                self.store.find_similar_documentation(datasource, request['question'], 10)
                for datasource in self.datasources
            ]
        results = await asyncio.gather(*tasks)


        logger.info("sorting retrieved documents")
        for index, out in enumerate(results):
            opt_doc = []
            if out and len(out) > 0 and out[0]['distances'] < self.context_relevance_threshold:
                distances = [doc['distances'] for doc in out]
                if len(out) > 5:
                    clusters = Container.clustering().kmeans(distances, 2)
                    shortest_cluster = clusters[0]
                    for doc in out:
                        if doc['distances'] in shortest_cluster:
                            opt_doc.append(doc)
                else:
                    opt_doc = out

            if "rag" not in response:
                response["rag"]= {"context" : {}}
            response["rag"]["context"][list(self.datasources.keys())[index]] = opt_doc

        return await super().handle(response)





