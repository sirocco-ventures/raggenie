from .formatter import Formatter
from loguru import logger
import requests
from app.base.base_plugin import BasePlugin
from app.base.remote_data_plugin import RemoteDataPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin
from typing import  Tuple, Optional
from app.readers.base_reader import BaseReader


class Website(BasePlugin, PluginMetadataMixin,RemoteDataPlugin,  Formatter):
    """
    Website class for interacting with website data.
    """

    def __init__(self, website_url:str):
        super().__init__(__name__)

        self.connection = {}

        # common
        self.params = {
            'url': website_url,
        }


    def connect(self):
        """
        Mocked connection method for Website.

        :return: Tuple containing connection status (True/False) and an error message if any.
        """
        return True, None


    def healthcheck(self)-> Tuple[bool, Optional[str]]:
        """
        Perform a health check by checking if the Website  is accessible.

        :return: Tuple containing the health status (True/False) and error message (if any).
        """
        logger.info("health check for website")

        url = self.params["url"]


        try:
            response = requests.get(url)
            if response.status_code == 200:
                logger.info("Website health check passed.")
                return True, None
            else:
                logger.error(f"Health check failed: {response.status_code} {response.text}")
                return False, "Failed to connect with airtable"
        except Exception as e:
            logger.exception(f"Exception during health check: {str(e)}")
            return False, str(e)


    def fetch_data(self, params=None):
        base_reader = BaseReader({
                                "type": "url",
                                "path": [self.params.get('url')]
                            })
        data = base_reader.load_data()
        return data
