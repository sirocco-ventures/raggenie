from app.plugins.postgresql.handler import Postresql
from app.plugins.bigquery.handler import Bigquery
from app.plugins.airtable.handler import Airtable
from app.plugins.website.handler import Website
from app.plugins.webhook.handler import Webhook
from loguru import logger

class DSLoader:
    def __init__(self, configs):
        self.config = configs

    def load_ds(self):
        db_classes = {
            "postgres": Postresql,
            "bigquery": Bigquery,
            "airtable": Airtable,
            "website": Website,
            "webhook": Webhook,
        }
        db_type = self.config.get("type")
        connection_params = self.config.get("params")

        logger.info(f"initialising {db_type}")

        db_class = db_classes.get(db_type)
        if db_class:
            try:
                ds = db_class(**connection_params)
                return ds
            except Exception as e:
                raise e

        else:
            logger.warning("Invalid database type specified in configuration.")
            return None