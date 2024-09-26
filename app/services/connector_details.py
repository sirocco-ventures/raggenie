from typing import  Any
from app.plugins.loader import DSLoader
from app.loaders.base_loader import BaseLoader
from loguru import logger

from app.repository import connector as repo
from sqlalchemy.orm import Session

def test_inference_provider_connection(inference):
    model_configs = [{
        "unique_name": inference.name,
        "name": inference.model,
        "api_key": inference.apikey,
        "endpoint": inference.endpoint,
        "kind" : inference.llm_provider,
    }]
    logger.info(f"model_configs:{model_configs}")
    inference_model = BaseLoader(model_configs= model_configs).load_model(inference.name)
    output, response_metadata = inference_model.do_inference(
            "hi", []
    )
    logger.info(f"output:{output}")
    if "error" in output:
        return None, output['error']
    return True, "Test Credentials successfully completed"


def test_plugin_connection(db_configs, config, provider_class):
    params = {}
    for conf in db_configs:
        if conf.slug not in config.provider_config:
            return None, f"Missing required config key: {conf.slug}"
        else:
            params[conf.field] = config.provider_config[conf.slug]

    params = {
        "type": provider_class,
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

def get_plugin_metadata(db_configs, config, provider_class):

    params = {}
    for conf in db_configs:
        if conf.slug not in config:
            return {}, Exception(f"Missing required config key: {conf.slug}")
        else:
            params[conf.field] = config.get(conf.slug, "")
    params = {
        "type": provider_class,
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
