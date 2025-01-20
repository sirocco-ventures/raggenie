from .formatter import Formatter
from loguru import logger
import sqlite3
import pandas as pd
from app.base.base_plugin import BasePlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin
from typing import Tuple, Optional, List
import uuid
import sqlparse
import sqlvalidator
import os


class CSVPlugin(BasePlugin, PluginMetadataMixin, Formatter):
    """
    CSVPlugin class for interacting with CSV data and inserting it into an SQL database.
    """

    def __init__(self, connector_name : str, document_files: List[str]):
        super().__init__(__name__)
        
        self.connector_name = connector_name.replace(' ','_')
        self.params = {
            'csv_files': document_files,
            'db_name': f"{self.connector_name}.sqlite",
        }
        self.connection = None
        self.max_limit = 10

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def connect(self) -> Tuple[bool, Optional[str]]:
        """
        Establish a connection to the SQLite database, delete all tables,
        and insert data from CSV files.

        :return: Tuple containing connection status (True/False) and an error message if any.
        """
        try:
            db_path = f"assets/datasource/csv_db/{self.params['db_name']}"
            if 'db_name' not in self.params or not self.params['db_name']:
                raise ValueError("Database name is missing or invalid in parameters.")
                        
            if os.path.exists(db_path):
                # Delete the file
                os.remove(db_path)
                print(f"The database file '{db_path}' has been deleted successfully.")

            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            self.connection = sqlite3.connect(
                db_path, 
                uri=True, 
                check_same_thread=False, 
                timeout=8.0
            )
            self.connection.row_factory = self._dict_factory
            self.cursor = self.connection.cursor()
            logger.info(f"Connected to database: {db_path}")
                        
            # Insert data from CSV files into the database
            for csv_file in self.params.get('csv_files', []):
                if 'file_name' not in csv_file or 'file_path' not in csv_file:
                    logger.warning(f"Invalid CSV file entry: {csv_file}")
                    continue

                table_name = csv_file['file_name'].rsplit('.', 1)[0].replace(' ','_')
                self._insert_csv_to_db(csv_file['file_path'], table_name)
            
            return True, None
        except Exception as e:
            logger.exception(f"Failed to connect to database: {type(e).__name__}, {e}")
            return False, f"{type(e).__name__}: {e}"


    def healthcheck(self):
        try:
            if self.connection is None:
                logger.warning("Connection to CSV is not established.")
                return False, "Connection to CSV is not established."

            self.cursor.execute("SELECT 1;")
            return True, None        
        except sqlite3.Error as error:
            return False, error

    def _insert_csv_to_db(self, csv_file: str, table_name: str):
        """
        Helper method to read a CSV file and insert its data into an SQLite table.

        :param csv_file: Path to the CSV file.
        :param table_name: Name of the table to insert data into.
        """
        try:
            # Read CSV file using pandas
            df = pd.read_csv(csv_file)
            logger.info(f"Read CSV file: {csv_file} with {len(df)} rows.")

            # Write to the SQLite database
            df.to_sql(table_name, self.connection, if_exists='replace', index=False)
            logger.info(f"Data from {csv_file} inserted into table: {table_name}")
        except Exception as e:
            logger.exception(f"Failed to insert data from {csv_file} into table {table_name}: {str(e)}")

    def configure_datasource(self, init_config):
        pass

    def fetch_data(self, query, params=None):
        try:
            params = {} if params is None else params
            self.cursor.execute(query, params)
            if "limit"  not in query.lower():
                return self.cursor.fetchmany(self.max_limit), None
            else:
                return self.cursor.fetchall(), None
        except Exception as e:
            logger.critical(e)
            self.connection.rollback()
            return None, e

    def fetch_schema_details(self):
        #Creating ddl from table schema
        table_metadata = []
        schema_ddl = []

        table_schemas=self._fetch_table_schema()

        if len(table_schemas) != 0 :

            for table, columns in table_schemas.items():
                table_ddl = ""

                schema = {
                    "table_id": str(uuid.uuid4()),
                    "table_name": table,
                    "description": "",
                    "columns": []
                }

                fields= []
                table_ddl = f"\n\nCREATE TABLE {table} ("
                for column in columns:
                    fields.append({
                        "column_id" : str(uuid.uuid4()),
                        "column_name": column['name'].replace('-','_'),
                        "column_type": column['type'],
                        "description": "",
                    })
                    table_ddl +=f"\n{column['name']} {column['type']} ,"
                table_ddl +=f");"

                schema["columns"] = fields
                table_metadata.append(schema)
                schema_ddl.append(table_ddl)

        return schema_ddl, table_metadata

    def create_ddl_from_metadata(self,table_metadata):
        schema_ddl = []
        for table in table_metadata:
            tmp = f"\n\nCREATE TABLE {table['table_name']}"
            for field in table["columns"]:
                tmp = f"{tmp} {field.get('column_name','')} \n"
            schema_ddl.append(tmp)
        return schema_ddl
    
    def _fetch_table_schema(self):
        # Execute query to get all table names 
        self.cursor.execute("SELECT name FROM sqlite_master")
        # Fetch all table names
        table_names = self.cursor.fetchall()

        table_schemas = {}

        for table in table_names:
            self.cursor.execute(f"SELECT name, type FROM pragma_table_info('{table['name']}')")
            columns = self.cursor.fetchall()

            table_schemas[table['name']] = columns
        return table_schemas

    def fetch_feedback(self):
        pass


    def validate(self,formated_sql):
        #validate sql using SQLParser
        queries = sqlparse.split(formated_sql)
        query = queries[0]
        formated_query = sqlparse.format(query, reindent=True, keyword_case='upper')

        parsed = sqlparse.parse(formated_query)[0]

        if parsed.get_type() != 'SELECT':
            return "Sorry, I am not designed for data manipulation operations"

        token_names = [p._get_repr_name() for p in parsed.tokens]
        if "DDL" in token_names:
            return "Sorry, I am not designed for data manipulation operations"

        sql_query = sqlvalidator.parse(formated_sql)
        if not sql_query.is_valid():
            logger.info(sql_query.is_valid())
            return "I didn't get you, Please reframe your question"

        return  None

    def close_conection(self):
        self.cursor.close()
        self.connection.close()