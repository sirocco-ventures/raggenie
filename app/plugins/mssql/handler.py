import pyodbc
from loguru import logger
import sqlvalidator
import sqlparse
from .formatter import Formatter
import uuid

from app.base.base_plugin import BasePlugin
from app.base.query_plugin import QueryPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin


class Mssql(Formatter, BasePlugin, QueryPlugin,  PluginMetadataMixin):

    def __init__(self, db_name:str, db_user:str, db_password:str, db_server:str="localhost", db_port:int=1433):
        logger.info("Initializing datasource")
        super().__init__(__name__)

        self.params = {
            'database': db_name,
            'user': db_user,
            'password': db_password,
            'server': db_server,
            'port': db_port,
        }
        self.connection = None

        self.cursor = None
        self.max_limit = 10000


    def connect(self):
        try:
            drivers = [driver for driver in pyodbc.drivers()]
            connection_string = f"DRIVER={{{drivers[0]}}};SERVER={self.params['server']};DATABASE={self.params['database']};UID={self.params['user']};PWD={self.params['password']}"
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            logger.info("Connection to MsSQL DB successful.")
            return True, None
        except pyodbc.Error as error:
            logger.error(f"Error connecting to MsSQL DB: {error}")
            return False, str(error)

    def healthcheck(self):
        try:
            if self.connection is None:
                logger.warning("Connection to MsSQL DB is not established.")
                return False, "Connection to MsSQL DB is not established."

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchall() 
                return True, None
        except pyodbc.Error as error:
            logger.error(f"Error during healthcheck: {error}")
            return False, str(error)


    def configure_datasource(self, init_config):
        pass

    def fetch_data(self, query, reconnect_attempt = True, params=None):
        try:
            self.cursor.execute(query)

            # Fetch column names
            column_names = [column[0] for column in self.cursor.description]

            # Fetch data
            if "TOP" not in query.upper():
                rows = self.cursor.fetchmany(self.max_limit)
            else:
                rows = self.cursor.fetchall()

            # Map column names to row data
            result = [dict(zip(column_names, row)) for row in rows]

            return result, None
        except pyodbc.Error as error:
            logger.error(f"Error executing query: {error}")
            if '08S01' in str(error) and reconnect_attempt:
                logger.info("Attempting to reconnect...")
                self.connect()  # Attempt to reconnect
                reconnect_attempt = False
                self.fetch_data(self, query, reconnect_attempt = False)
            return None, str(error)

    def fetch_schema_details(self):
        schema_ddl = []
        table_metadata = []
        # Execute query to get all table names and schemas in the database
        self.cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
        tables = self.cursor.fetchall()
        print(f"tables:{tables}")
        
        for table in tables:
            schema_name = table[0]
            table_name = table[1]

            logger.info(f"Fetching DDL for table: {schema_name}.{table_name}")
            
            schema = {
                    "table_id": str(uuid.uuid4()),
                    "table_name": f"{schema_name}.{table_name}",
                    "description": "",
                    "columns": []
                }
            # Fetch column details for the current table
            self.cursor.execute(f"""
                    SELECT 
                        COLUMN_NAME,
                        DATA_TYPE,
                        CHARACTER_MAXIMUM_LENGTH,
                        IS_NULLABLE,
                        COLUMN_DEFAULT
                    FROM 
                        INFORMATION_SCHEMA.COLUMNS
                    WHERE 
                        TABLE_SCHEMA = '{schema_name}'
                        AND TABLE_NAME = '{table_name}';
                """)
            columns = self.cursor.fetchall()

            # Start building the DDL statement
            ddl = f"CREATE TABLE {schema_name}.{table_name} (\n"
            fields= []

            # Loop through each column and add its definition to the DDL
            for column in columns:
                column_name = column[0]
                data_type = column[1]
                max_length = column[2]
                is_nullable = column[3]
                column_default = column[4]
                fields.append({
                        "column_id" : str(uuid.uuid4()),
                        "column_name": column_name,
                        "column_type": data_type,
                        "description": "",
                    })
                
                schema["columns"] = fields

                table_metadata.append(schema)

                # Format data type with length if applicable
                if max_length:
                    data_type = f"{data_type}({max_length})"
                
                # Add NULL/NOT NULL constraint
                nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                
                # Handle column default value if any
                default = f"DEFAULT {column_default}" if column_default else ""

                # Add the column definition to the DDL
                ddl += f"    {column_name} {data_type} {nullable} {default},\n"

            # Remove the last comma and newline, then close the statement
            ddl = ddl.rstrip(",\n") + "\n);\n\n"

            table_metadata.append(schema)

            # Append the DDL statement for the current table to schema_ddl
            schema_ddl.append(ddl)
        # print(f"table_metadata:{table_metadata}")

        return schema_ddl, table_metadata

    def create_ddl_from_metadata(self,table_metadata):
        schema_ddl = []
        for table in table_metadata:
            tmp = f"\n\nCREATE TABLE {table['table_name']}"
            for field in table["columns"]:
                tmp = f"{tmp} {field.get('column_name','')} \n"
            schema_ddl.append(tmp)
        return schema_ddl


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

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


