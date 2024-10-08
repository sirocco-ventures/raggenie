from .formatter import Formatter
from loguru import logger
import requests
import json
from app.base.base_plugin import BasePlugin
from app.base.messaging_plugin import MessagePlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin
from typing import  Tuple, Optional
from app.readers.base_reader import BaseReader


class Webhook(BasePlugin, PluginMetadataMixin, MessagePlugin, Formatter):
    """
    Website class for interacting with website data.
    """

    def __init__(self, webhook_url:str, webhook_method: str, webhook_headers: dict):
        super().__init__(__name__)

        self.connection = {}

        # common
        self.params = {
            'url': webhook_url,
            'headers': webhook_headers,
            'method': webhook_method
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
        logger.info("health check for webhook")

        url = self.params.get('url')
        method = self.params.get('method').upper()

        try:
            match method:
                case 'POST':
                    response = requests.post(url)
                case 'PUT':
                    response = requests.put(url)
                case 'GET':
                    response = requests.get(url)
                case _:
                    logger.error(f"Unsupported method: {method}")
                    return False, f"Unsupported method: {method}"
            response = requests.get(url)
            if response.status_code != 404:
                logger.info("Website health check passed.")
                return True, None
            else:
                logger.error(f"Health check failed: {response.status_code} {response.text}")
                return False, "Failed to connect with airtable"
        except Exception as e:
            logger.exception(f"Exception during health check: {str(e)}")
            return False, str(e)


    def send(self, params:dict=None):
        if params is None:
            params = {}
            
        url = self.params.get('url')
        method = self.params.get('method').upper()
        header_string = self.params.get('headers', '{}')
        
        try:
            headers = json.loads(header_string)
        except Exception as e:
            logger.warning("improper json for headers")
            headers = {}

        try:
            match method:
                case 'POST':
                    response = requests.post(url, headers=headers, data=params)
                case 'PUT':
                    response = requests.put(url, headers=headers, data=params)
                case 'GET':
                    response = requests.get(url, headers=headers, params=params)
                case _:
                    logger.error(f"Unsupported method: {method}")
                    return False, f"Unsupported method: {method}"
                
            if response.status_code < 300:
                logger.info(f"Successfully sent data to webhook. Status code: {response.status_code}")
                return True, response
            else:
                logger.error(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
                return False, response
            
        except Exception as e:
            logger.exception(f"Exception during {method} request: {str(e)}")
            return False, str(e)
