import chromadb
from chromadb import Settings
import yaml
from loguru import logger
import time
import flatdict
import ast
from app.base.base_vectordb import BaseVectorDB
from app.providers.config import configs





class ChromaDataBase(BaseVectorDB):
    def __init__(self, path:str="./vector_db", embeddings: dict={"provider": "chroma_default", "vectordb": "chroma"}):
        logger.info("initializing with configs")
        self.client = None
        self.embedding_function = None
        self.params = {
            'path': path,
            'settings': Settings(allow_reset=True),
        }
        self.embeddings = embeddings


    def connect(self):
        try:
            self.client = chromadb.PersistentClient(**self.params)
            if configs.indexing_enabled:
                self.client.reset()
            self.embedding_function = self.load_embeddings_function()

            self.schema_store = self.client.get_or_create_collection(
                name="schema_store",
                embedding_function = self.embedding_function,
                )
            self.documentation_store = self.client.get_or_create_collection(
                name="documentation_store",
                embedding_function = self.embedding_function
                )
            self.samples_store = self.client.get_or_create_collection(
                name="samples_store",
                embedding_function = self.embedding_function
                )
            self.cache_store = self.client.get_or_create_collection(
                name="cache_store",
                embedding_function = self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Connected to ChromaDB")
            return None
        except Exception as e:
            logger.critical(f"Failed connecting ChromaDB: {e}")
            return str(e)
        
    def clear_collection(self, config_id):
        self.config_id = config_id
        self.schema_store.delete(where={"config_id": config_id})
        self.cache_store.delete(where={"config_id": config_id})
        self.documentation_store.delete(where={"config_id": config_id})
        self.samples_store.delete(where={"config_id": config_id})
        

    def health_check(self):
        pass



    def load_yaml_data(self, yaml_path):
        with open(yaml_path, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        start_time = time.time()
        for i in range(len(data_loaded)):
            self.store.add(
                documents=[data_loaded[i]["description"]],
                metadatas=[data_loaded[i]["metadata"]],
                ids=["id_"+str(i)]
            )
        end_time = time.time()
        response_time = end_time - start_time
        logger.info(f"vector db insertion time -> yaml loading : {response_time}")

    # Function to convert list values to a string representation
    def _convert_lists_to_strings(self,d):
        for key, value in d.items():
            if isinstance(value, list):
                d[key] = str(value)
            elif isinstance(value, dict):
                self._convert_lists_to_strings(value)
        return d

    def prepare_data(self,datasource_name, chunked_document, chunked_schema, queries, config_id):
        logger.info("Inserting into vector store")
        logger.info(f"datasource_name:{datasource_name}")
        start_time = time.time()
        if chunked_document:
            doc_count = self.documentation_store.count()
            for i, doc in enumerate(chunked_document, start = doc_count):
                self._add_to_store(doc.page_content, {**doc.metadata, "datasource": datasource_name, "config_id": config_id}, self.documentation_store, i)

        if chunked_schema:
            schema_count = self.schema_store.count()
            for i, doc in enumerate(chunked_schema, start = schema_count):
                self._add_to_store(doc.page_content, {**doc.metadata, "datasource": datasource_name, "config_id": config_id}, self.schema_store, i)

        if queries:
            cache_count = self.schema_store.count()
            for j,doc in enumerate(queries, start = cache_count):
                doc = self._convert_lists_to_strings(doc)
                doc = flatdict.FlatDict(doc, delimiter='.')

                self._add_to_store(doc['description'], {**dict(doc['metadata']), "datasource": datasource_name, "config_id": config_id}, self.samples_store, j)
                self._add_to_store(doc['description'], {**dict(doc['metadata']), "datasource": datasource_name, "config_id": config_id}, self.cache_store, j)


        logger.info("Created vector store for the source documents")
        end_time = time.time()
        response_time = end_time - start_time
        logger.info(f"vector db insertion time -> source docs : {response_time}")

    def _add_to_store(self, document, metadata, store, index):
        store.add(
            documents=[document],
            metadatas=[metadata],
            ids=["id_" + str(index)]
        )

    def update_cache(self, document, metadata):
        try:
            self.cache_store.add(
                documents=[document],
                metadatas=[metadata],
                ids=["id_" + str(self.cache_store.count()+1)]
            )
            logger.info("cache updated successfully")
        except:
            logger.info("error updating cache")


    def _convert_strings_to_lists(self, d):
        for key, value in d.items():
            if isinstance(value, str) and '[' in value and ']' in value:
                d[key] = ast.literal_eval(value)
            elif isinstance(value, dict):
                self._convert_strings_to_lists(value)

        return d

    def unflatten_dict(self,flat_dict):
        unflat_dict = {}
        for key, value in flat_dict.items():
            parts = key.split('.')
            d = unflat_dict
            for part in parts[:-1]:
                if part not in d:
                    d[part] = {}
                d = d[part]
            d[parts[-1]] = value

        unflat_dict = self._convert_strings_to_lists(unflat_dict)
        return unflat_dict


    async def _find_similar(self, datasource, query, store, sample_count=3):
        res = store.query(
            query_texts=[query],
            n_results=sample_count,
            where={"datasource": datasource}  # Filter by the datasource in the metadata
        )


        output = []
        if len(res["ids"]) > 0:
            for i in range(len(res["ids"][0])):
                output.append({
                    "document": res["documents"][0][i],
                    "id": res["ids"][0][i],
                    "metadatas": self.unflatten_dict(res["metadatas"][0][i]),
                    "distances": res["distances"][0][i]

                })


        return output

    def update_store(self, ids = None, metadatas = None, documents = None):
        if ids is None:
            ids = "id_" + str(self.samples_store.count()+1)

        self.samples_store.upsert(
            ids = ids,
            metadatas = metadatas,
            documents = documents
        )

    def update_weights(self,results,increment_value = 1):
        results['metadatas'][0]['weights'] += increment_value

        self.update_store(results['ids'],results['metadatas'],results['documents']
        )


    def _find_by_id(self, id_d, store):
        results = store.get(
            ids= [id_d]
        )
        logger.info(f"Suggestion weights:{results}")

        output = []
        if len(results["ids"]) > 0:
            for i in range(len(results["ids"])):
                output.append({
                    "document": results["documents"][i],
                    "id": results["ids"][i],
                    "metadatas": self.unflatten_dict(results["metadatas"][i])

                })
        self.update_weights(results)
        return output

    async def find_similar_documentation(self, datasource, query, count):
        return await self._find_similar(datasource, query, self.documentation_store, count)

    async def find_similar_schema(self, datasource, query, count):
        return await self._find_similar(datasource, query, self.schema_store, count)

    async def find_samples_by_id(self, id):
        return await self._find_by_id(id, self.samples_store)

    async def find_similar_cache(self, datasource, query, count = 3):
        return await self._find_similar(datasource, query, self.samples_store, count)