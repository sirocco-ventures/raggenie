from .formatter import Formatter
from loguru import logger
import requests
from app.base.base_plugin import BasePlugin
from app.base.remote_data_plugin import RemoteDataPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin
from app.base.document_data_plugin import DocumentDataPlugin
from typing import  Tuple, Optional
from app.readers.base_reader import BaseReader


class Document(BasePlugin, PluginMetadataMixin,DocumentDataPlugin,  Formatter):
    """
    Document class for interacting with document data.
    """

    def __init__(self, document_file:str):
        super().__init__(__name__)

        self.connection = {}

        # common
        self.params = {
            'document_file': document_file,
        }


    def connect(self):
        """
        Mocked connection method for pdf.

        :return: Tuple containing connection status (True/False) and an error message if any.
        """
        return True, None


    def healthcheck(self)-> Tuple[bool, Optional[str]]:
        """
        Perform a health check by checking if the document is accessible.

        :return: Tuple containing the health status (True/False) and error message (if any).
        """
        logger.info("health check for documentations")
        
        try:
            data = self.fetch_data(params=None)
            if not data:
                raise ValueError("No data fetched during health check")
            logger.info("Checking documentation")
            return True, None
        except Exception as e:
            logger.exception(f"Exception during fetching data: {str(e)}")
            return False, str(e)

    def fetch_data(self, params=None):
        data = []
        supported_types = {".pdf": "pdf", ".docx": "docx", ".txt": "txt", ".yaml": "yaml"}

        for file_info in self.params.get("document_file", []):
            url = file_info.get("file_path")
            if url is None:
                logger.error("URL is missing in the document file information.")
                continue
            
            file_type = None
            
            for ext, typ in supported_types.items():
                if url.endswith(ext):
                    file_type = typ
                    break

            if file_type is None:
                logger.error(f"Unsupported file format: {url}")
                continue

                
            base_reader = BaseReader({
                "type": file_type,
                "path": [url]
            })
            data.extend(base_reader.load_data())

        return data


