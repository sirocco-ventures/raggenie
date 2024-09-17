from app.plugins.postgresql.handler import Postresql
from app.plugins.bigquery.handler import Bigquery
from app.plugins.airtable.handler import Airtable
from loguru import logger


import sys

class DSLoader:
    def __init__(self, configs):
        self.config = configs

    def load_ds(self):
        db_classes = {
            "postgres": Postresql,
            "bigquery": Bigquery,
            "airtable": Airtable
        }
        db_type = self.config.get("type")
        connection_params = self.config.get("params")
        
        logger.info("initialising " + db_type)
        init_scripts = self.config.get("init")

        db_class = db_classes.get(db_type)
        if db_class:
            try:
                ds = db_class(**connection_params)
                err = ds.configure_datasource(init_scripts)
                if err:
                    logger.warning("Unable to run init configurations")
                    return None
                return ds
            except Exception as e:
                raise e
            
        else:
            logger.warning("Invalid database type specified in configuration.")
            return None