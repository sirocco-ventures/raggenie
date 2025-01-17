import pymssql
from loguru import logger
import sqlvalidator
import sqlparse
from .formatter import Formatter
import uuid

from app.base.base_plugin import BasePlugin
from app.base.query_plugin import QueryPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin


class Mssql(Formatter, BasePlugin, QueryPlugin,  PluginMetadataMixin):

    def __init__(self, connector_name : str, db_name:str, db_user:str, db_password:str, db_host:str="localhost", db_port:int=1433):
        logger.info("Initializing datasource")
        super().__init__(__name__)

        self.connector_name = connector_name.replace(' ','_')
        self.params = {
            'database': db_name,
            'user': db_user,
            'password': db_password,
            'server': db_host,
            'port': db_port,
        }
        self.connection = None

        self.cursor = None
        self.max_limit = 10000


    def connect(self):
        try:
            self.connection = pymssql.connect(**self.params)
            self.cursor = self.connection.cursor(as_dict=True)
            logger.info("Connection to MsSQL DB successful.")
            return True, None
        except pymssql.Error as error:
            logger.error(f"Error connecting to MsSQL DB: {error}")
            return False, error

    def healthcheck(self):
        try:
            if self.connection is None:
                logger.warning("Connection to MsSQL DB is not established.")
                return False, "Connection to MsSQL DB is not established."

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchall() 
                return True, None
        except pymssql.Error as error:
            logger.error(f"Error during healthcheck: {error}")
            return False, error


    def configure_datasource(self, init_config):
        pass

    def fetch_data(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            if "TOP" not in query.upper():
                return self.cursor.fetchmany(self.max_limit), None
            else:
                return self.cursor.fetchall(), None
        except pymssql.Error as e:
            return None, e

    def fetch_schema_details(self):
        schema_ddl = []
        table_metadata = []
        # Execute query to get all table names and schemas in the database
        self.cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
        tables = self.cursor.fetchall()
        
        for table in tables:
            schema_name = table['TABLE_SCHEMA']
            table_name = table['TABLE_NAME']

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
                column_name = column['COLUMN_NAME']
                data_type = column['DATA_TYPE']
                max_length = column['CHARACTER_MAXIMUM_LENGTH']
                is_nullable = column['IS_NULLABLE']
                column_default = column['COLUMN_DEFAULT']
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


