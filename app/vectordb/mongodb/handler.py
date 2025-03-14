import pymongo
from loguru import logger
from app.base.base_vectordb import BaseVectorDB
import urllib.parse
import certifi


class AltasMongoDB(BaseVectorDB):
    def __init__(self, uri: str , embeddings: dict={"provider": "default", "vectordb": "mongodb"}):
        self.uri = uri
        self.client = None
        self.embeddings = embeddings
        self.EMBEDDING_FIELD_NAME = "embeddings"

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.uri, tlsCAFile=certifi.where())
            logger.info(f"Connected to Altas MongoDB Vector Database")
            self.db = self.client.get_database('context_store')
            self.schema_collection = self.db.get_collection('schema')
            self.doc_collection = self.db.get_collection('documents')
            self.cache_collection = self.db.get_collection('cache')
            # self.clear_collection()
            self.schema_index_name = "schema"
            self.doc_index_name = "doc"
            self.cache_index_name = "cache"
            self.emf = self.load_embeddings_function()
            return None
        except Exception as e:
            logger.critical(f"Failed connecting Altas MongoDB Vector Database: {e}")
            return str(e)

    def health_check(self):
        try:
            sample = {
                    "_id": "doc1",
                    "datasource":"psql_db",
                    "document": "This referes to the user data which consist of username, password, email and address",
                    "metadata":{
                        "username": "username"
                    }
                }
            sample[self.EMBEDDING_FIELD_NAME] = self.generate_embedding(sample['document'])

            self.doc_collection.insert_many([sample])
            # self.schema_collection.insert_many([sample])
            # self.cache_collection.insert_many([sample])

            collection_list = self.db.list_collection_names()
            logger.info(f"collections available:{collection_list}")
            self.doc_collection.delete_many({ "datasource": "psql_db" })
            if len(collection_list) > 0:
                return None
            else:
                return "Collections cannot be created in DB"

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return f"Failed to connect with Altas MongoDB {e}"


    def clear_collection(self, config_id):
    #     self.schema_collection.delete_many({})  # Delete all documents in the collection
    #     self.doc_collection.delete_many({})
    #     self.cache_collection.delete_many({})
        self.config_id = config_id
        self.cache_collection.delete_many({ "metadata.config_id": config_id })
        self.schema_collection.delete_many({ "metadata.config_id": config_id })
        self.doc_collection.delete_many({ "metadata.config_id": config_id })

    def generate_embedding(self, context: str) -> list[float]:
        array = self.emf([context])[0]
        return array.tolist()

    def prepare_data(self, datasource_name, chunked_document, chunked_schema, queries, config_id):
        if chunked_document:
            documents = []
            document_count = self.doc_collection.count_documents({})
            for i, doc in enumerate(chunked_document, start = document_count):
                sample = {
                    # "_id": "doc" + str(i),
                    "document": doc.page_content,
                    "metadata": {**doc.metadata,"datasource": datasource_name, "config_id": config_id}
                }
                sample[self.EMBEDDING_FIELD_NAME] = self.generate_embedding(sample['document'])
                documents.append(sample)

            self.doc_collection.insert_many(documents)

        if chunked_schema:
            schemas = []
            schema_count = self.schema_collection.count_documents({})
            for i, doc in enumerate(chunked_schema, start = schema_count):
                sample = {
                    # "_id": "doc" + str(i),
                    "document": doc.page_content,
                    "metadata": {**doc.metadata,"datasource": datasource_name, "config_id": config_id}
                }
                sample[self.EMBEDDING_FIELD_NAME] = self.generate_embedding(sample['document'])
                schemas.append(sample)
            self.schema_collection.insert_many(schemas)

        if queries:
            caches = []
            queries_count = self.cache_collection.count_documents({})
            for i, doc in enumerate(queries, start = queries_count):
                sample = {
                    # "_id": "doc" + str(i),
                    "document": doc['description'],
                    "metadata": {**doc['metadata'], "datasource": datasource_name, "config_id": config_id}
                }
                sample[self.EMBEDDING_FIELD_NAME] = self.generate_embedding(sample['document'])
                caches.append(sample)

            self.cache_collection.insert_many(caches)

        self.create_knn_index()

    def _create_index(self, collection, index_name):
        index = list(collection.list_search_indexes())

        if len(index)==0:
            collection.create_search_index({
                "definition": {
                    "mappings": {
                        "dynamic": True,
                        "fields": {
                            self.EMBEDDING_FIELD_NAME: {
                                "dimensions": 384,
                                "similarity": "cosine",
                                "type": "knnVector"
                            }
                        }
                    }
                },
                "name": index_name  # Renamed for consistency
            })
            logger.info(f"Index created:{index_name}")

        else:
            logger.info(f"{index_name} Index already exists")


    def create_knn_index(self):
        self._create_index(self.doc_collection, self.doc_index_name)
        self._create_index(self.schema_collection, self.schema_index_name)
        self._create_index(self.cache_collection, self.cache_index_name)

    async def _find_similar(self, datasource, collection, query, count, index_name):
        logger.info(f"datasources:{datasource}")
        logger.info(f"collection:{collection}")
        logger.info(f"index_name:{index_name}")


        res = collection.aggregate([

            {
                '$vectorSearch': {
                    "index": index_name,
                    "path": self.EMBEDDING_FIELD_NAME,
                    "queryVector": self.generate_embedding(query),
                    "numCandidates": 50,
                    "limit": count,

                }
            },
            {
            '$match': {
                'metadata.datasource': datasource  # Filter for the specified datasource
            }
            },
            {
            "$project": {
            "_id" : 1,
            "datasource" : 1,
            "document": 1,
            "metadata": 1,
            "score": {"$meta": "vectorSearchScore"}
            }
        }
        ])
        results = list(res)
        for result in results:
            result['distances'] = 1 - result['score']
        return results

    async def find_similar_schema(self, datasource, query,count):
       return await self. _find_similar(datasource, self.schema_collection, query, count, self.schema_index_name)

    async def find_similar_documentation(self, datasource, query, count):
       return await self. _find_similar(datasource, self.doc_collection, query, count, self.doc_index_name)

    async def find_similar_cache(self, datasource, query,count = 3):
       return await self. _find_similar(datasource, self.cache_collection, query, count, self.cache_index_name)