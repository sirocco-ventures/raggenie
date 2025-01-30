from typing import  Any
from app.plugins.loader import DSLoader
from loguru import logger

from app.repository import connector as repo
from sqlalchemy.orm import Session
from app.vectordb import chromadb, mongodb, loader


def test_plugin_connection(db_configs, config, provider_class):
    params = {}
    for conf in db_configs:
        if conf.slug not in config.provider_config:
            return None, f"Missing required config key: {conf.slug}"
        else:
            params[conf.field] = config.provider_config[conf.slug]

    params = {
        "type" : provider_class,
        "connector_name" : config.connector_name,
        "params": params,
    }

    datasource = DSLoader(params).load_ds()
    success, err = datasource.connect()

    if not success and err:
        return None, f"Test Credentials Failed: {str(err)}"

    success, err = datasource.healthcheck()
    if not success and err:
        return None, f"Connection to {provider_class} is not established: {str(err)}"

    return True, "Test Credentials successfully completed"

def get_plugin_metadata(db_configs, config, connector_name, provider_class):

    params = {}
    for conf in db_configs:
        if conf.slug not in config:
            return {}, Exception(f"Missing required config key: {conf.slug}")
        else:
            params[conf.field] = config.get(conf.slug, "")
    params = {
        "type" : provider_class,
        "connector_name" : connector_name,
        "params": params,
    }

    datasource = DSLoader(
            params
        ).load_ds()

    success, err=datasource.connect()

    if not success and err:
        return {}, Exception("Test Credentials Failed")


    success, err = datasource.healthcheck()
    if not success and err:
        logger.warning("Datasource health failed")
        return {}, Exception("Connection to "+provider_class+" is not established")

    schema_ddl, schema_config = datasource.fetch_schema_details()
    if len(schema_config) > 0:
        return schema_config, None
    else:
        return {}, Exception("Failed to fetch schema details")


def check_configurations_availability(db: Session)-> Any:
    conf, is_error = repo.getbotconfiguration(db)

    if (conf == [] or conf==None) or is_error:
        return "Configuration Not Found"

    inference, is_error = repo.get_inference_by_id(conf.id,db)
    if (inference == [] or inference==None) or is_error:
        return "Inference configuration not found"

    connectors, is_error = repo.get_all_connectors(db)
    if (connectors == [] or connectors==None) or is_error:
        return "Connector not found"

    return None


def test_vector_db_credentials(db_config, config, key):
    if isinstance(db_config.config, list):
        configs = [i.get("slug") for i in db_config.config if isinstance(i, dict)]
        flag = any(con == d_conf for con in configs for d_conf in config.vectordb_config)

        if not flag:
            return f"Missing required config key: {db_config.key}", True

        vectordb_config = config.vectordb_config.copy()
        vectordb_config.pop("key", None)
        vectorloader = loader.VectorDBLoader(config={"name":db_config.key, "params":vectordb_config}).load_class()
        err = vectorloader.connect()

        if err is not None:
            return f"Failed to connect to {db_config.key}: {err}", True

        err = vectorloader.health_check()

        if err is not None:
            return f"Failed to connect to {db_config.key}: {err}", True

    return f"{db_config.key} Test Credential Successfully Completed", False






