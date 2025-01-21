from .formatter import Formatter
from loguru import logger
import requests
import uuid
from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode
from app.base.base_plugin import BasePlugin
from app.base.query_plugin import QueryPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin
from typing import Tuple, Optional


class Airtable(BasePlugin, QueryPlugin, PluginMetadataMixin, Formatter):
    """
    Airtable class for interacting with Airtable API and fetching table data, schemas, and more.
    """

    def __init__(self, token:str, workspace:str):
        super().__init__(__name__)

        self.connection = {
            "base_url": "https://api.airtable.com/v0",
        }

        # common
        self.params = {
            'token': token,
            'base_id': workspace
        }


    def connect(self):
        """
        Mocked connection method for Airtable.

        :return: Tuple containing connection status (True/False) and an error message if any.
        """
        return True, None


    def healthcheck(self)-> Tuple[bool, Optional[str]]:
        """
        Perform a health check by checking if the Airtable base is accessible.

        :return: Tuple containing the health status (True/False) and error message (if any).
        """
        logger.info("health check for airtable")

        url = self.connection["base_url"]+ "/meta/bases/"+ self.params["base_id"]+"/tables"

        headers = {
            "Authorization": "Bearer "+self.params["token"]
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                logger.info("Airtable health check passed.")
                return True, None
            else:
                logger.error(f"Health check failed: {response.status_code} {response.text}")
                return False, "Failed to connect with airtable"
        except Exception as e:
            logger.exception(f"Exception during health check: {str(e)}")
            return False, str(e)



    def configure_datasource(self, init_config):
        """
        Configures the Airtable datasource.

        :param init_config: Initial configuration for the datasource.
        """
        return None


    def fetch_data(self, query, params=None):
        """
        Fetches data from Airtable based on the provided query.

        :param query: The Airtable API query.
        :param params: Optional query parameters.
        :return: A tuple containing the fetched data and an optional error message.
        """

        logger.info("preparing query")
        try:
            parts = query.split("v0")
            if len(parts) <= 1:
                return [], "Invalid query format"

            query = parts[1].lstrip('/')
            first_part, second_part = query.split('/', 1)
            final_query = second_part


            url = self.connection.get("base_url")+"/"+self.params["base_id"]+"/"+final_query

            headers = {
                "Authorization": "Bearer "+self.params["token"]
            }

            logger.info(f"Generating URL for fetch_data: {url}")
            url_parts = urlsplit(url)
            query_params = parse_qs(url_parts.query)
            query_params.pop('api_key', None)
            query_params.pop('API_KEY', None)
            new_query_string = urlencode(query_params, doseq=True)
            url = urlunsplit((url_parts.scheme, url_parts.netloc, url_parts.path, new_query_string, url_parts.fragment))

            logger.info(f"Final request URL: {url}")
            response = requests.get(url, headers=headers, params=params)


            if response.status_code == 200:
                return response.json(), None
            else:
                logger.error(f"Failed to fetch data: {response.status_code}, {response.text}")
                return [], "Failed to fetch"

        except Exception as e:
            logger.error(f"Failed to fetch data: {e}")
            return [], "Failed to fetch"


    def fetch_schema_details(self):
        """
        Fetches the schema details (tables and columns) from Airtable.

        :return: A tuple containing the schema DDL as a list of strings and the table metadata.
        """

        schema_ddl = []
        table_metadata = []

        base_id = self.params.get("base_id")
        token = self.params.get("token","")
        base_url = self.connection.get("base_url")

        url = f"{base_url}/meta/bases/{base_id}/tables"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            out = response.json()
            if "tables" in out and len(out["tables"])>0:
                tables = out["tables"]
                for table in tables:
                    schema = {
                            "table_id": str(uuid.uuid4()),
                            "table_name": table["name"],
                            "description": "",
                            "columns": []
                    }
                    fields= []
                    for field in table["fields"]:
                        fields.append({
                            "column_id" : str(uuid.uuid4()),
                            "column_name": field['name'],
                            "column_type": field['type'],
                            "description": "",
                        })

                    schema["columns"] = fields
                    schema_ddl.append(f"\nTable name: {table['name']}\n" + "\n".join([f['column_name'] for f in fields]))
                    table_metadata.append(schema)

        return schema_ddl, table_metadata

    def create_ddl_from_metadata(self,table_metadata):
        """
        Creates DDL from the provided table metadata.

        :param table_metadata: List of table metadata dictionaries.
        :return: List of schema DDL strings.
        """
        schema_ddl = []
        for table in table_metadata:
            ddl = f"\nTable name: {table['table_name']}\n"
            ddl += "\n".join([col.get("column_name","") for col in table["columns"]])
            schema_ddl.append(ddl)
        return schema_ddl


    def validate(self, formatted_sql: str) -> None:
        """
        Validates the provided SQL.

        :param formatted_sql: SQL string to validate.
        """
        pass

    def close_connection(self) -> None:
        """
        Closes the connection to Airtable.
        """
        pass

