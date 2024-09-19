from google.cloud import bigquery
from google.oauth2 import service_account
from .formatter import Formatter
from loguru import logger
import re
from typing import List
import json
import uuid
from app.base.base_plugin import BasePlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin
from app.base.query_plugin import QueryPlugin


class Bigquery(Formatter, BasePlugin, QueryPlugin,  PluginMetadataMixin):

    def __init__(self, project_id: str, service_account_json: str):
        super().__init__(__name__)

        self.params = {
            'project' : project_id,
            'credentials' : service_account.Credentials.from_service_account_info(json.loads(service_account_json)),
        }
        self.client = None


        self.schema = []

    def connect(self):
        """
        Establish a connection to BigQuery.
        :return: Tuple containing connection status and an optional error message.
        """
        try:
            self.client = bigquery.Client(**self.params)

            logger.info("Connection to Google Bigquery successful.")
            return True, None
        except Exception as error:
            logger.error(f"Error connecting to Google Bigquery: {error}")
            return False, str(error)

    def healthcheck(self):
        """
        Perform a health check by executing a simple query.
        :return: Tuple containing the health check status and an optional error message.
        """
        if self.client is None:
            logger.warning("Connection to BigQuery is not established.")
            return False, "Connection to BigQuery is not established."
        try:
            query = 'SELECT schema_name FROM `region-us`.INFORMATION_SCHEMA.SCHEMATA LIMIT 1'
            query_job = self.client.query(query)
            results = query_job.result()

            if results.total_rows > 0:
                logger.info("Healthcheck successful: BigQuery connection is healthy.")
                return True, None
            else:
                logger.warning("Healthcheck failed: No results returned.")
                return False, "Healthcheck failed: No results returned."

        except Exception as error:
            logger.error(f"Healthcheck failed: {error}")
            return False, str(error)

    def configure_datasource(self, init_config):

        return None

    def fetch_data(self,query: str):
        """
        Fetch data by executing a BigQuery SQL query.
        :param query: SQL query string.
        :return: Tuple of data rows and an optional error message.
        """
        try:
            query = self.client.query(query)
            results = query.result()
            rows = [row for row in results]
            return rows, None
        except Exception as e:
            logger.critical(e)
            return None, e

    def fetch_schema_details(self):
        """
        Fetch schema details for all tables in all datasets.
        :return: A tuple containing the schema DDLs and table metadata.
        """

        schema_ddl = []
        table_metadata = []

        if self.client is None:
            logger.error("BigQuery client is not connected.")
            return schema_ddl, table_metadata

        datasets = list(self.client.list_datasets())
        if not datasets:
            logger.critical("Project does not contain any datasets.")
            return schema_ddl, table_metadata

        for dataset in datasets:
            dataset_id = dataset.dataset_id
            schema_structure_query = f"SELECT * FROM {dataset_id}.INFORMATION_SCHEMA.TABLES"
            result, error = self.fetch_data(schema_structure_query)

            if result is not None:
                for res in result:

                    schema = {
                        "table_id": str(uuid.uuid4()),
                        "table_name":  f"{dataset.dataset_id}.{res[2]}",
                        "description": "",
                        "columns": []
                    }
                    fields= []

                    ddl = res[11]

                    # Regex to extract column names and data types
                    pattern = r'`([^`]+)`\s(\w+)|(\w+)\s(\w+)'

                    matches = re.findall(pattern, ddl)

                    # Extract column names and data types from the matches
                    columns = [match[0] or match[2] for match in matches]
                    data_types = [match[1] or match[3] for match in matches]

                    for index,(column, datatype) in enumerate(list(zip(columns, data_types))[1:]):
                        fields.append({
                            "column_id" : str(uuid.uuid4()),
                            "column_name": column,
                            "column_type": datatype,
                            "description": "",
                        })
                    schema["columns"] = fields

                    table_metadata.append(schema)
                    schema_ddl.append(ddl)

            else:
                logger.critical(f"Error fetching schema:{error}")


        return schema_ddl, table_metadata



    def create_ddl_from_metadata(self, table_metadata: List[dict]):
        """
        Create DDL statements from table metadata.
        :param table_metadata: List of table metadata.
        :return: List of DDL strings.
        """
        schema_ddl = []
        for table in table_metadata:
            tmp = f"CREATE TABLE '{table['table_name']}'"
            for index,field in enumerate(table["columns"]):
                if index == 0:
                    tmp = f"{tmp} ({field.get('column_name','')} {field.get('column_type','')}"
                elif index < len(table['columns'])-1:
                    tmp = f"{tmp},{field.get('column_name','')} {field.get('column_type','')}"
                else:
                    tmp = f"{tmp},{field.get('column_name','')} {field.get('column_type','')});"

            schema_ddl.append(tmp)
        return schema_ddl


    def validate(self, formatted_query: str) -> None:
        """
        Validate the formatted query (placeholder for actual implementation).
        :param formatted_query: SQL query string.
        """
        pass