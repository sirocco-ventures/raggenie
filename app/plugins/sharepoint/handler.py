from .formatter import Formatter
from loguru import logger
import requests
from app.base.base_plugin import BasePlugin
from app.base.remote_data_plugin import RemoteDataPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin
from typing import Tuple, Optional
from app.readers.base_reader import BaseReader

class SharePoint(BasePlugin, PluginMetadataMixin, RemoteDataPlugin, Formatter):
    """
    SharePoint class for interacting with SharePoint data.
    """

    def __init__(self, site_url: str, client_id: str, client_secret: str, tenant_id: str):
        super().__init__(__name__)

        self.connection = {}

        # SharePoint connection parameters
        self.params = {
            'site_url': site_url,
            'client_id': client_id,
            'client_secret': client_secret,
            'tenant_id': tenant_id,
        }

    def connect(self) -> Tuple[bool, Optional[str]]:
        """
        Establish a connection to the SharePoint site using the provided credentials.

        :return: Tuple containing connection status (True/False) and an error message if any.
        """
        logger.info("Attempting to connect to SharePoint site")

        try:
            # Mocking connection setup to SharePoint
            # You might need to implement OAuth authentication here to get an access token
            # For example, you could use Microsoft's Authentication Library (MSAL) or similar
            logger.info("Successfully connected to SharePoint")
            return True, None
        except Exception as e:
            logger.exception(f"Failed to connect to SharePoint: {str(e)}")
            return False, str(e)

    def healthcheck(self) -> Tuple[bool, Optional[str]]:
        """
        Perform a health check by checking if the SharePoint site is accessible.

        :return: Tuple containing the health status (True/False) and error message (if any).
        """
        logger.info("Performing health check for SharePoint")

        site_url = self.params["site_url"]

        try:
            # Replace with actual SharePoint endpoint check if necessary
            response = requests.get(site_url)
            if response.status_code == 200:
                logger.info("SharePoint health check passed.")
                return True, None
            else:
                logger.error(f"Health check failed: {response.status_code} {response.text}")
                return False, "Failed to connect to SharePoint site"
        except Exception as e:
            logger.exception(f"Exception during health check: {str(e)}")
            return False, str(e)

    def fetch_data(self, params=None):
        """
        Fetch data from SharePoint using a base reader.

        :param params: Additional parameters for data retrieval if needed.
        :return: Data fetched from the SharePoint site.
        """
        logger.info("Fetching data from SharePoint")

        base_reader = BaseReader({
            "type": "sharepoint",
            "path": [self.params.get('site_url')]
        })
        data = base_reader.load_data()
        return data
