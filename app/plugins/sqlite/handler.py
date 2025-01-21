import sqlite3
import pathlib
import urllib
from loguru import logger
import sqlvalidator
import sqlparse
from .formatter import Formatter
import uuid

from app.base.base_plugin import BasePlugin
from app.base.query_plugin import QueryPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin

class Sqlite(Formatter, BasePlugin, QueryPlugin, PluginMetadataMixin):
    def __init__(self, db_name:str, db_parent_path:str=''):
        logger.info("Initializing datasource")
        super().__init__(__name__)

        self.params = {
            'db_name': db_name,
            'db_parent_path': db_parent_path,
        }
        self.connection = None

        # class specific
        self.cursor = None
        self.max_limit = 5

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    def _path_to_uri(self, path):
        path = pathlib.Path(path)
        if path.is_absolute():
            return path.as_uri()
        return 'file:' + urllib.parse.quote(path.as_posix(), safe=':/')

    def connect(self):
        try:
            db_path = pathlib.Path(self.params['db_parent_path']).joinpath(self.params['db_name']).as_posix()
            uri_filename = f"{self._path_to_uri(db_path)}?mode=rw"            
            self.connection = sqlite3.connect(uri_filename, uri=True, check_same_thread=False, timeout= 8.0)
            self.connection.row_factory = self._dict_factory
            self.cursor = self.connection.cursor()
            
            logger.info("Connection to SQLite DB successful.")
            return True, None
        except sqlite3.Error as error:
            logger.error(f"Error connecting to SQLite DB: {error}")
            return False, error

    def healthcheck(self):
        try:
            if self.connection is None:
                logger.warning("Connection to SQLite DB is not established.")
                return False, "Connection to SQLite DB is not established."

            self.cursor.execute("SELECT 1;")
            return True, None        
        except sqlite3.Error as error:
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
                # logger.info(f"columns:{columns}")
                for column in columns:
                    fields.append({
                        "column_id" : str(uuid.uuid4()),
                        "column_name": column['name'],
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

            # logger.info(f"table_name:{table['name']}")
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
