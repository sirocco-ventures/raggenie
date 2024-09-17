from sqlalchemy.orm import Session
import app.repository.connector as repo
import app.repository.provider as config_repo
import app.schemas.connector as schemas
from fastapi import HTTPException
from sqlalchemy import create_engine, MetaData
from app.services import provider as provider_svc
from typing import List
import requests
from loguru import logger
from app.services.connector_details import get_plugin_metadata
import yaml
from fastapi import Request



def list_connectors(db: Session):
    connectors, is_error = repo.get_all_connectors(db)

    if is_error:
        return connectors, "DB Error"

    if not connectors:
        return [], None

    connectors_response = [schemas.ConnectorResponse(
        connector_id=connector.id,
        connector_type=connector.connector_type,
        connector_name=connector.connector_name,
        connector_description=connector.connector_description,
        connector_config=connector.connector_config,
        schema_config=connector.schema_config,
        connector_docs=connector.connector_docs,
        connector_key=connector.provider.key,
        enable=connector.enable,
        icon=connector.provider.icon
    ) for connector in connectors]

    return connectors_response, None

def get_connector(connector_id: int, db: Session):
    connector, is_error = repo.get_connector_by_id(connector_id, db)

    if is_error:
        return connector, "DB Error"

    if connector is None:
        return [], None

    connector_response = schemas.ConnectorResponse(
        connector_id=connector.id,
        connector_type=connector.connector_type,
        connector_name=connector.connector_name,
        connector_description=connector.connector_description,
        connector_config=connector.connector_config,
        connector_key=connector.provider.key,
        schema_config=connector.schema_config,
        connector_docs=connector.connector_docs,
        enable=connector.enable,
        icon=connector.provider.icon
    )

    return connector_response, None 

def download_and_save_pdf(connector_name: str, url: str) -> str:
    response = requests.get(url)
    connector_name = connector_name.replace(" ", "_")
    file_path = f"./assets/source_{connector_name}.pdf"
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

def create_connector(connector: schemas.ConnectorBase, db: Session):
    provider, is_error = config_repo.get_provider_by_id(connector.connector_type, db)
    if is_error:
        return provider, "DB Error"
    
    
    
    provider_configs, is_error = config_repo.get_config_types(connector.connector_type, db)

    if is_error:
        return None, "DB Error"
    
    if provider.category_id == 2:

        schema_details, is_error = get_plugin_metadata(provider_configs, connector.connector_config, provider.key)

        if is_error is None:
            connector.schema_config = schema_details
            
            new_connector, is_error = repo.create_new_connector(connector, db)

            if is_error:
                return None, "Failed to create connector"

            connector_response = schemas.ConnectorResponse(
                connector_id=new_connector.id,
                connector_type=new_connector.connector_type,
                connector_name=new_connector.connector_name,
                connector_description=new_connector.connector_description,
                connector_config=new_connector.connector_config,
                connector_key=new_connector.provider.key,
                schema_config=new_connector.schema_config,
                connector_docs=new_connector.connector_docs,
                enable=new_connector.enable
            )

            return connector_response, None
        else:
            return None, is_error
    
    else:
        return None, "Invalid Connector Type."
    



def update_connector(connector_id: int, connector: schemas.ConnectorUpdate, db: Session):
    updated_connector, is_error = repo.update_existing_connector(connector_id, connector, db)

    if is_error:
        return updated_connector, "DB Error"

    if updated_connector is None:
        return [], None
    
    connector_response = schemas.ConnectorResponse(
        connector_id=updated_connector.id,
        connector_type=updated_connector.connector_type,
        connector_name=updated_connector.connector_name,
        connector_description=updated_connector.connector_description,
        connector_config=updated_connector.connector_config,
        schema_config=updated_connector.schema_config,
        connector_docs=updated_connector.connector_docs,
        enable=updated_connector.enable
    )
    
    return connector_response, None

def delete_connector(connector_id: int, db: Session):
    deleted_connector, is_error = repo.delete_connector_by_id(connector_id, db)

    if is_error:
        return deleted_connector, "DB Error"

    if deleted_connector is None:
        return [], None

    connector_response = schemas.ConnectorResponse(
        connector_id=deleted_connector.id,
        connector_type=deleted_connector.connector_type,
        connector_name=deleted_connector.connector_name,
        connector_description=deleted_connector.connector_description,
        connector_config=deleted_connector.connector_config,
        schema_config=deleted_connector.schema_config,
        connector_docs=deleted_connector.connector_docs,
        enable=deleted_connector.enable
    )
    
    return connector_response, None


def updateschemas(connector_id: int, connector: schemas.SchemaUpdate, db: Session):
    updated_connector, is_error = repo.update_existing_connector(connector_id, connector, db)

    if is_error:
        return updated_connector, "DB Error"

    if updated_connector is None:
        return [], None

    connector_response = schemas.SchemaUpdate(
        schema_config=updated_connector.schema_config,
    )

    return connector_response, None



def list_configurations(db: Session):
    configurations, is_error = repo.get_all_configurations(db)

    if is_error:
        return configurations, "DB Error"
    
    if not configurations:
        return [], None

    config_list = [schemas.ConfigurationResponse(
        id=config.id,
        name=config.name,
        short_description=config.short_description,
        long_description=config.long_description,
        status=config.status,
        capabilities=[schemas.CapabilitiesBase(
            id=capabilities.id,
            name=capabilities.name,
            requirements=capabilities.requirements,
            description=capabilities.description,
            config_id=capabilities.config_id,
        ) for capabilities in config.capabilities],
        inference=[schemas.InferenceResponse(
            id=inference_mapping.inference.id,
            name=inference_mapping.inference.name,
            apikey=inference_mapping.inference.apikey,
            llm_provider=inference_mapping.inference.llm_provider,
            model=inference_mapping.inference.model,
            endpoint=inference_mapping.inference.endpoint,
            config_id=inference_mapping.config_id
        ) for inference_mapping in config.inference_mapping]
    ) for config in configurations]

    return config_list, None

def create_configuration(configuration: schemas.ConfigurationCreation, db: Session):
    new_config, is_error = repo.create_new_configuration(configuration, db)
    if is_error:
        return new_config, "DB Error"
    
    if not new_config:
        return [], None
    


    config_response = schemas.ConfigurationResponse(
        id=new_config.id,
        name=new_config.name,
        short_description=new_config.short_description,
        long_description=new_config.long_description,
        status=new_config.status,
        capabilities=[schemas.CapabilitiesBase(
            id=capabilities.id,
            name=capabilities.name,
            requirements=capabilities.requirements,
            description=capabilities.description,
            config_id=capabilities.config_id,
        ) for capabilities in new_config.capabilities],
    )

    return config_response, None

def update_configuration(config_id: int, configuration: schemas.ConfigurationUpdate, db: Session):
    updated_config, is_error = repo.update_existing_configuration(config_id, configuration, db)

    if is_error:
        return updated_config, "DB Error"
    
    if updated_config is None:
        return [], None
    
    config_response = schemas.ConfigurationResponse(
        id=updated_config.id,
        name=updated_config.name,
        short_description=updated_config.short_description,
        long_description=updated_config.long_description,
        status=updated_config.status,
        capabilities=[schemas.CapabilitiesBase(
            id=capabilities.id,
            name=capabilities.name,
            requirements=capabilities.requirements,
            description=capabilities.description,
            config_id=capabilities.config_id,
        ) for capabilities in updated_config.capabilities],
    )

    return config_response, None


def create_capabilities(capabilities: schemas.CapabilitiesBase, db: Session):
    new_capability, is_error = repo.create_capability(capabilities, db)

    if is_error:
        return new_capability, "DB Error"
    
    if capabilities.actions_list:
        result, is_mapping_error = repo.create_capability_action_mappings(
            capability_id=new_capability.id, 
            action_ids=capabilities.actions_list, 
            db=db
        )
        if is_mapping_error:
            return result, "DB Error while creating capability-action mappings"
    
    capability_response = schemas.CapabilitiesBase(
        id=new_capability.id,
        name=new_capability.name,
        description=new_capability.description,
        requirements=new_capability.requirements,
        config_id=new_capability.config_id,
        actions=[{
        "id": mapping.actions.id,
        "name": mapping.actions.name,
        "description": mapping.actions.description,
        "types": mapping.actions.types,
        "table": mapping.actions.table,
        "enable": mapping.actions.enable,
        } for mapping in new_capability.cap_actions_mapping]
    )
    
    return capability_response, None


def get_all_capabilities(db: Session):
    capabilities, is_error = repo.get_all_capabilities(db)

    if is_error:
        return capabilities, "DB Error"
    
    if not capabilities:
        return [], None

    capabilities_response = []
    
    for cap in capabilities:        
        capabilities_response.append(
            schemas.CapabilitiesBase(
                id=cap.id,
                name=cap.name,
                description=cap.description,
                requirements=cap.requirements,
                config_id=cap.config_id,
                actions=[{
                "id": mapping.actions.id,
                "name": mapping.actions.name,
                "description": mapping.actions.description,
                "types": mapping.actions.types,
                "table": mapping.actions.table,
                "enable": mapping.actions.enable,
                } for mapping in cap.cap_actions_mapping]
            )
        )
    
    return capabilities_response, None

def update_capability(cap_id: int, capability: schemas.CapabilitiesUpdateBase, db: Session):
    updated_capability, is_error = repo.update_capability(cap_id, capability, db)

    if is_error:
        return updated_capability, "DB Error"
    
    if not updated_capability:
        return [], None
    
    capability_response = schemas.CapabilitiesBase(
        id=updated_capability.id,
        name=updated_capability.name,
        description=updated_capability.description,
        requirements=updated_capability.requirements,
        config_id=updated_capability.config_id,
        actions=[{
            "id": mapping.actions.id,
            "name": mapping.actions.name,
            "description": mapping.actions.description,
            "types": mapping.actions.types,
            "table": mapping.actions.table,
            "enable": mapping.actions.enable,
            } for mapping in updated_capability.cap_actions_mapping]
    )
    
    return capability_response, None

def delete_capability(cap_id: int, db: Session):
    deleted, is_error = repo.delete_capability(cap_id, db)

    if is_error:
        return deleted, "DB Error"
    
    if not deleted:
        return [], None
    
    return True, None



            

def get_inference_and_plugin_configurations(db: Session):
    configuration={}
    connectors, status = repo.get_all_connectors(db)
    if status:
        return configuration
    configs, is_error = repo.getbotconfiguration(db)
    if configs is None:
        configuration["models"]=[]
    else:
        inference, is_error = create_inference_yaml(configs.id, db)
        configuration["models"] = inference
    
    datasources = []

    for conn in connectors:
        provider, is_error = config_repo.get_provider_by_id(conn.connector_type, db)
        if is_error:
            continue
        datasource = formatting_datasource(conn, provider)
        if datasource:
            datasource['name'] = str(conn.connector_name).replace(" ", "_").lower()
            datasource['description'] = conn.connector_description
            datasources.append(datasource)
    configuration["datasources"] = datasources
    return configuration

def create_inference_yaml(config_id:int, db:Session):

    inference, is_error = repo.get_inferences_by_config_id(config_id, db)

    if is_error:
        return inference, "Inference configuration not found"
    
    inference_yaml = []

    for inf in inference:
        model_data = {
            "unique_name": inf.inference.name,
            "name": inf.inference.model,
            "api_key": inf.inference.apikey,
            "endpoint": inf.inference.endpoint,
            "kind": inf.inference.llm_provider,
        }
        inference_yaml.append(model_data)

    return inference_yaml, None

def create_yaml_file(request:Request,config_id: int, db: Session):
    configuration, is_error = repo.get_configuration_by_id(config_id, db)
    if (configuration == [] or configuration==None) or is_error:
        return None, None, "Configuration Not Found"
        
    inferences, is_error = repo.get_inferences_by_config_id(config_id, db)
    if (inferences == [] or inferences==None) or is_error:
        return None, None, "Inference configuration not found"

    connectors, is_error = repo.get_all_connectors(db)
    if (connectors == [] or connectors==None) or is_error:
        return None, None, "Connector not found"
    
    for connector in connectors:
        sqls, is_error = provider_svc.getsqlbyconnector(connector.id, db)

        if is_error:
            logger.error(f"Error getting SQL from connector {connector.id}", is_error)
            continue
        
        for sql in sqls:
            if provider_svc.insertVectorStore(request, sql, db):
                logger.error(f"Error inserting SampleSQL into vector store for connector {connector.id}")
        
    datasources = []
    for conn in connectors:
        provider, is_error = config_repo.get_provider_by_id(conn.connector_type, db)
        if is_error:
            continue
        datasource = formatting_datasource(conn, provider)
        if datasource:
            datasource['name'] = str(conn.connector_name).replace(" ", "_").lower()
            datasource['description'] = conn.connector_description
            schema_config = conn.schema_config
            datasource['schema_config'] = schema_config
            datasources.append(datasource)
    
    documentations = datasources
    use_case = dict({
        'short_description': configuration.short_description,
        'long_description': configuration.long_description,
        'capabilities': [
                {
                "name": cap.name if cap.name else "default",
                "description": cap.description if cap.description else "No description provided",
                "requirements": cap.requirements if cap.requirements else [],
                "analysis": [],
                "action": {}
                } for cap in configuration.capabilities
         ]
    })
    
    if documentations is not None and use_case is not None:
        repo.update_configuration_status(config_id,db)    
    return documentations, use_case, None



def formatting_datasource(connector, provider):
    
    
    
    if provider.category_id == 1:
        return {
            'type': 'default',
            'params': {'skip': True},
            'documentations': [{'type': 'pdf', 'path': [connector.connector_config.get('local_url')]}]
        }
    elif provider.category_id == 2:
        return {
            'type': provider.key,
            'params': connector.connector_config,
            'documentations': [{'type': 'text', 'value': connector.connector_docs}]
        }
    else:
        return None
    

def get_inference(inference_id: int, db: Session):
    inference, is_error = repo.get_inference_by_id(inference_id, db)

    if is_error:
        return inference, "DB Error"
    
    if inference is None:
        return [], None
    
    data = schemas.InferenceResponse(
        name=inference.name,
        apikey=inference.apikey,
        model=inference.model,
        endpoint=inference.endpoint,
        llm_provider=inference.llm_provider,
        id=inference.id
    )
    
    return data, None

def create_inference(inference: schemas.InferenceBase, db: Session):
    inference_created, is_error = repo.create_inference(inference, db)
    
    if is_error:
        return inference_created, "DB Error"
    
    data = schemas.InferenceResponse(
        name=inference_created.name,
        apikey=inference_created.apikey,
        model=inference_created.model,
        endpoint=inference_created.endpoint,
        llm_provider=inference_created.llm_provider,
        id=inference_created.id
    )

    return data, None

def update_inference(inference_id: int, inference: schemas.InferenceBaseUpdate, db: Session):
    updated_inference, is_error = repo.update_inference(inference_id, inference, db)

    if is_error:
        return updated_inference, "DB Error"
    
    if updated_inference is None:
        return [], None
    
    data = schemas.InferenceResponse(
        name=updated_inference.name,
        apikey=updated_inference.apikey,
        model=updated_inference.model,
        endpoint=updated_inference.endpoint,
        llm_provider=updated_inference.llm_provider,
        id=updated_inference.id
    )

    return data, None

def list_actions(db:Session):

    actions, is_error = repo.list_actions(db)

    if is_error:
        return actions, "DB Error"
    
    if actions is None:
        return [], None
    
    return [
        schemas.ActionsResponse(
            id=action.id,
            name=action.name,
            description=action.description,
            types=action.types,
            condition=action.condition,
            table = action.table,
            connector_id=action.connector_id,
            enable = action.enable,
            ) for action in actions], False
    
def get_actions(action_id:int, db:Session):

    action, is_error = repo.get_action_by_id(action_id, db)

    if is_error:
        return action, "DB Error"
    
    if action is None:
        return [], None
    
    return schemas.ActionsResponse(
        id=action.id,
        name=action.name,
        description=action.description,
        types=action.types,
        condition=action.condition,
        table = action.table,
        connector_id=action.connector_id,
        enable = action.enable,
    ), False

def get_actions_by_connector(connector_id:int, db:Session):

    actions, is_error = repo.get_actions_by_connector(connector_id, db)

    if is_error:
        return actions, "DB Error"
    
    if actions is None:
        return [], None
    
    return [
        schemas.ActionsResponse(
            id=action.id,
            name=action.name,
            description=action.description,
            types=action.types,
            condition=action.condition,
            table = action.table,
            connector_id=action.connector_id,
            enable = action.enable,
            ) for action in actions], False
    
def create_action(action: schemas.Actions, db:Session):

    action_created, is_error = repo.create_action(action, db)

    if is_error:
        return action_created, "DB Error"
    
    return schemas.ActionsResponse(
        id=action_created.id,
        name=action_created.name,
        description=action_created.description,
        types=action_created.types,
        condition=action_created.condition,
        table = action_created.table,
        connector_id=action_created.connector_id,
        enable = action_created.enable,
    ), False
    
def get_use_cases(db: Session):
    configurations, status = repo.get_all_configurations(db)
    use_cases = []
    for conf in configurations:
        use_case = {}
        use_case['short_description'] = conf.short_description
        use_case['long_description'] = conf.long_description
        use_case['capabilities'] = []
        capabilities = [cap for cap in conf.capabilities]
        for cap in capabilities:
            capability = {}
            capability['name'] = cap.name
            capability['description'] = cap.description
            capability['requirements'] = cap.requirements
            use_case['capabilities'].append(capability)
        use_cases.append(use_case)

    if len(use_cases) > 0:
        return use_cases[0]
    else:
        return {
            "short_description": "",
            "long_description": "",
            "capabilities": []
        }