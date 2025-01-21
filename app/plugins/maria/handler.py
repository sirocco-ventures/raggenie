import mariadb
from loguru import logger
import sqlvalidator
import sqlparse
from .formatter import Formatter
import uuid

from app.base.base_plugin import BasePlugin
from app.base.query_plugin import QueryPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin


class Maria(Formatter, BasePlugin, QueryPlugin,  PluginMetadataMixin):

    def __init__(self, db_name:str, db_user:str="root", db_password:str="", db_host:str="localhost", db_port:int=3306):
        logger.info("Initializing datasource")
        super().__init__(__name__)
        
        db_port = int(db_port)

        # common
        self.params = {
            'database': db_name,
            'user': db_user,
            'password': db_password,
            'host': db_host,
            'port': db_port,
        }
        self.connection = None

        # class specific
        self.cursor = None
        self.max_limit = 5
        


    def connect(self):
        try:
            self.connection = mariadb.connect(**self.params)
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("Connection to MariaDB successful.")
            return True, None
        except mariadb.Error as error:
            logger.error(f"Error connecting to MariaDB: {error}")
            return False, error

    def healthcheck(self):
        try:
            if self.connection is None:
                logger.warning("Connection to MariaDB is not established.")
                return False, "Connection to MariaDB is not established."

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchall() 
                return True, None
        except mariadb.Error as error:
            logger.error(f"Error during healthcheck: {error}")
            return False, error


    def configure_datasource(self, init_config):
        logger.info("Configuring datasource")
        if init_config is not None and "script" in init_config:
            try:
                self.cursor.execute(init_config["script"])
                self.connection.commit()
            except Exception as e:
                return e

        return None

    def fetch_data(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            if "limit"  not in query.lower():
                return self.cursor.fetchmany(self.max_limit), None
            else:
                return self.cursor.fetchall(), None
        except mariadb.Error as e:
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
                table_ddl = f"\n\nCREATE TABLE {table}"
                for column in columns:
                    fields.append({
                        "column_id" : str(uuid.uuid4()),
                        "column_name": column['column_name'],
                        "column_type": column['data_type'],
                        "description": "",
                    })
                    table_ddl +=f"\n{column['column_name']} {column['data_type']} {column['character_maximum_length']},"
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
        # Execute query to get all table names in the public schema
        self.cursor.execute("SHOW TABLES")
        # Fetch all table names
        table_names = self.cursor.fetchall()

        table_schemas = {}

        for table in table_names:

            table_name = next(iter(table.values()))
            self.cursor.execute(f"SELECT column_name, data_type, IFNULL(character_maximum_length, '') AS character_maximum_length FROM information_schema.columns WHERE table_name = '{table_name}'")
            columns = self.cursor.fetchall()


            table_schemas[table_name] = columns
        return table_schemas

    def fetch_feedback(self):
        sql_query = "SELECT chat_query, feedback_json FROM public.chat_histories WHERE feedback_status = 2 AND created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY);"
        result = self.fetch_data(sql_query)
        logger.info(result)
        return result

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


