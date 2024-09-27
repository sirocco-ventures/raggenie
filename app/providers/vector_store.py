import chromadb
from chromadb import Settings
import yaml
from loguru import logger
import time
import flatdict
import ast


# import
from embeddings.loader import EmLoader


class Vectorstore:
    def __init__(self, config):
        logger.info("initializing with configs")
        logger.info(config)

        self.client = chromadb.PersistentClient(path=config["path"],settings=Settings(allow_reset=True))
        self.client.reset()
        self.embedding_function = EmLoader(config).load_embclass().load_emb()


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

    def prepare_data(self, chunked_document, chunked_schema, queries):
        logger.info("Inserting into vector store")
        start_time = time.time()
        for i, doc in enumerate(chunked_document):
            self._add_to_store(doc.page_content, {**doc.metadata, "type": "documentation"}, self.documentation_store, i)

        for i, doc in enumerate(chunked_schema):
            self._add_to_store(doc.page_content, {**doc.metadata, "type": "schema"}, self.schema_store, i)

        if queries:
            for j,doc in enumerate(queries,start = 1):
                doc = self._convert_lists_to_strings(doc)
                doc = flatdict.FlatDict(doc, delimiter='.')

                self._add_to_store(doc['description'], dict(doc['metadata']), self.samples_store, j+len(chunked_document))
                self._add_to_store(doc['description'], dict(doc['metadata']), self.cache_store, j+len(chunked_document))


        logger.info("Created vector store for the source documents")
        end_time = time.time()
        response_time = end_time - start_time
        logger.info(f"vector db insertion time -> source docs -> {response_time}")

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


    def _find_similar(self, query, store, sample_count=3):
        results = store.query(
            query_texts=[query],
            n_results=sample_count
        )

        output = []

        if len(results["ids"]) > 0:
            for i in range(len(results["ids"][0])):
                output.append({
                    "document": results["documents"][0][i],
                    "id": results["ids"][0][i],
                    "metadatas": self.unflatten_dict(results["metadatas"][0][i]),
                    "distances": results["distances"][0][i]

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

    def find_similar_documentation(self, query, sample_count=5):
        return self._find_similar(query, self.documentation_store, sample_count)

    def find_similar_schema(self, query, sample_count=5):
        return self._find_similar(query, self.schema_store, sample_count)

    def find_similar_samples(self, query, sample_count=3):
        output = self._find_similar(query, self.samples_store, sample_count)
        output = sorted(output, key=lambda d: int(float(d['metadatas']['weights'])),reverse = True)
        return output

    def find_samples_by_id(self, id):
        return self._find_by_id(id, self.samples_store)

    def find_similar_cache(self, query):
        return self._find_similar(query, self.samples_store)



