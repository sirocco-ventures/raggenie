from loguru import logger
# import pyPDF2
from app.providers.container import Container
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from app.readers.base_reader import BaseReader

class SourceDocuments:  
    def __init__(self,schema_details, schema_configs, documentation):
        self.documentation = []        
        logger.info("Fetching schema details")
        self.schema_details = schema_details
        self.schema_configs = schema_configs

        if documentation is not None and len(documentation) != 0:
            for docs in documentation:
                try:
                    reader = BaseReader(source=docs)
                    docs = reader.load_data()
                    self.documentation.extend(docs)
                except Exception as e:
                    logger.error(e)

        for schema_config in schema_configs:
            table_doc = ''
            table_doc = f"Table Name: {schema_config['table_name']} - {schema_config['description']}\n column are given below\n"
            for column in schema_config['columns']:
                table_doc = f"{table_doc} {column.get('column_name','')} - {column['description']}\n"
            self.documentation.append({'content': table_doc, 'metadata': {}})
            

                             
    def get_source_documents(self):
        chunked_docs = []
        chunked_schema = []
        
        try:

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20,separators=["\n\n","\'\")"])
            text_splitter_doc = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=20,separators=["\n\n","\n \n"])
            
            splitted_schema = list(map(lambda item: f"'{item}'", self.schema_details))
            load_schema = text_splitter.create_documents(splitted_schema)



            for docs in self.documentation:
                temp_docs = text_splitter_doc.create_documents([docs["content"]])
                chunks = text_splitter_doc.split_documents(temp_docs)
                for chunk in chunks:
                    chunk.metadata = docs["metadata"] if "metadata" in docs else {}
                chunked_docs.extend(chunks)
                
            chunked_schema = text_splitter.split_documents(load_schema)
        except Exception as e:
            logger.critical(e)

        
        return chunked_docs, chunked_schema

    



        
        





