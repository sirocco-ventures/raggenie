from app.base.abstract_handlers import AbstractHandler
from loguru import logger
from typing import Any, Optional
import numpy as np
from app.providers.container import Container



class SchemaRetriever(AbstractHandler):
    """
    A handler for retrieving similar schemas based on a given question and context.

    This class queries the store for schemas similar to the input question and context. It processes the
    retrieved schemas to potentially cluster them and select the most relevant schemas based on certain criteria.

    Attributes:
        store (object): The data store used to find similar schemas.
    """
    
    def __init__(self,store):
        """
        Initializes the SchemaRetriever with the provided store.

        Args:
            store (object): The data store used for schema retrieval.
        """
        self.store = store

    def handle(self, request: Any) -> str:
        """
        Retrieves similar schemas from the store and updates the response with the results.

        Args:
            request (Any): The incoming request containing the question, context, and filtering criteria.

        Returns:
            Dict[str, Any]: The updated response dictionary with retrieved schemas.
        """

        logger.info("passing through => schema_retriever")
        
        response = request
        
        datasources = request.get('rag_filters', {}).get("datasources", [])
        schema_count = request.get('rag_filters', {}).get("schema_count", 0)
        intent = request.get("intent_extractor", {}).get("intent", "")


        auto_context = "\n\n".join(cont.get("document", "") for cont in request.get("rag", {}).get("context", []))


        out = self.store.find_similar_schema(datasources, request["question"] + "\n" + auto_context, schema_count)
        
        if out and len(out) > 0:
            distances = [doc['distances'] for doc in out]
            if len(out) > 2 and intent != 'database_structure_and_metadata_inquiry':
                clusters = Container.clustering().kmeans(distances, 2)
                shortest_cluster = clusters[0]
                opt_doc = [doc for doc in out if doc.get('distances') in shortest_cluster]
            else:
                opt_doc = out

            response["rag"].update({
                 "schema":    opt_doc,
            })
        else:
            response["rag"].update({
                "schema": [],
            })
            
        return response
        




