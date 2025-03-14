from sqlalchemy.orm import Session
import app.repository.connector as repo
import app.repository.provider as config_repo
import app.schemas.connector as schemas
from app.services import provider as provider_svc
from app.schemas.provider import VectorDBResponse
import requests
import os
import uuid
from loguru import logger
from app.services.connector_details import get_plugin_metadata
from fastapi import Request
from app.providers.data_preperation import SourceDocuments
from app.loaders.base_loader import BaseLoader




def list_connectors(db: Session, user_id: str):

    """
    Retrieves all connector records from the database.

    Args:
        db (Session): Database session object.

    Returns:
        Tuple: List of connector responses and error message (if any).
    """

    connectors, is_error = repo.get_all_connectors(db, user_id)

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
        icon=connector.provider.icon,
        provider_id=connector.provider.category_id
    ) for connector in connectors]

    return connectors_response, None

def list_connectors_by_provider_category(category_ids: int, db: Session, user_id: str):
    """
    Retrieves all connector records from the database filtered by provider category.

    Args:
        category_id (int): The ID of the provider category.
        db (Session): Database session object.

    Returns:
        Tuple: List of connector responses and error message (if any).
    """
    connectors, error = list_connectors(db, user_id)

    if error:
        return [], error

    filtered_connectors = []
    for category_id in category_ids:
        filtered_connectors.extend([connector for connector in connectors if connector.provider_id == category_id])

    return filtered_connectors, None



def get_connector(connector_id: int, db: Session):

    """
    Retrieves the details of a specific connector by its ID.

    Args:
        connector_id (int): The ID of the connector.
        db (Session): Database session object.

    Returns:
        Tuple: Connector response and error message (if any).

    """


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

    """
    Downloads the PDF from the specified URL and saves it to the assets directory.

    Args:
        connector_name (str): Name of the connector.
        url (str): URL of the PDF to download.

        Returns:
            str: Path of the saved PDF file.
            str: Error message (if any).
    """


    response = requests.get(url)
    connector_name = connector_name.replace(" ", "_")
    file_path = f"./assets/source_{connector_name}.pdf"
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

async def fileValidation(file):

    """
    Validates the uploaded file for format and size constraints.

    Args:
        file (UploadFile): The uploaded document file.

    Returns:
        Tuple[str, int]: An error message if validation fails, or the size of the file if it passes.
    """

    if not file.filename.endswith((".pdf", ".txt", ".yaml", ".docx",".csv")):
        return "Invalid file format", None

    content = await file.read()
    file_size = len(content)

    await file.seek(0)

    max_file_size_bytes = 100 * 1024 * 1024
    if file_size > max_file_size_bytes:
        return "File size exceeds the limit", None

    return None, file_size


async def upload_pdf(file):
    """
    Uploads a document file to the specified connector.

    Args:
        file (UploadFile): The uploaded document file.

    Returns:
        Tuple: Connector response and error message (if any).
    """

    uuid_str = str(uuid.uuid4())
    file_path = f"./assets/datasource/documents/{uuid_str}/{file.filename}"

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(await file.read())

        return {"file_path": file_path,"file_id":uuid_str}, None
    except Exception as e:
        return None, f"Failed to write file: {str(e)}"


def create_connector(connector: schemas.ConnectorBase, db: Session, user_id: str):

    """
    Creates a new connector record in the database.

    Args:
        connector (ConnectorBase): The data for the new connector.
        db (Session): Database session dependency.

    Returns:
        Tuple: Connector response and error message (if any).
    """

    provider, is_error = config_repo.get_provider_by_id(connector.connector_type, db)
    if is_error:
        return provider, "DB Error"

    provider_configs, is_error = config_repo.get_config_types(connector.connector_type, db)

    if is_error:
        return None, "DB Error"

    match provider.category_id:
        case 2 | 5:
            logger.info("creating plugin with category database")
            schema_details, is_error = get_plugin_metadata(provider_configs, connector.connector_config, connector.connector_name, provider.key)
            if is_error is None:
                connector.schema_config = schema_details
            else:
                return None, "Failed to create connector"
        case 1:
            logger.info("creating plugin with category remote documents")
        case 3:
            logger.info("creating plugin with category messaging")
        case 4:
            logger.info("creating plugin with category offline documents")
        case _:
            return None, "Invalid Connector Type."

    new_connector, is_error = repo.create_new_connector(connector, db, user_id)
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



def update_connector(connector_id: int, connector: schemas.ConnectorUpdate, db: Session):

    """
    Updates an existing connector based on its ID.

    Args:
        connector_id (int): The ID of the connector to update.
        connector (ConnectorUpdate): The updated data for the connector.
        db (Session): Database session dependency.

    Returns:
        Tuple: Connector response and error message (if any).
    """

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

    """
    Deletes a connector based on its ID.

    Args:
        connector_id (int): The ID of the connector to delete.
        db (Session): Database session dependency.

    Returns:
        Tuple: Connector response and error message (if any).

    """

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

    """
    Updates the schema configuration for a connector.

    Args:
        connector_id (int): The ID of the connector.
        connector (SchemaUpdate): The updated schema configuration for the connector.
        db (Session): Database session dependency.
    Returns:
        Tuple: Schema update response and error message (if any).

    """

    updated_connector, is_error = repo.update_existing_connector(connector_id, connector, db)

    if is_error:
        return updated_connector, "DB Error"

    if updated_connector is None:
        return [], None

    connector_response = schemas.SchemaUpdate(
        schema_config=updated_connector.schema_config,
    )

    return connector_response, None


def get_inference_by_config_id(config_id:int , db:Session):
    """
    Retrieves the inference configuration based on the configuration ID.

    Args:
        config_id (int): The ID of the configuration.
        db (Session): Database session dependency.

    Returns:
        Tuple: Inference configuration response and error message (if any).
    """

    inference_mapping, is_error = repo.get_inference_by_config(config_id, db)

    if is_error:
        return inference_mapping, "DB Error"

    if inference_mapping is None:
        return schemas.InferenceResponse(), None

    return schemas.InferenceResponse(
        id=inference_mapping.inference.id,
        name=inference_mapping.inference.name,
        apikey=inference_mapping.inference.apikey,
        config_id=inference_mapping.inference.config_id,
        llm_provider=inference_mapping.inference.llm_provider,
        model=inference_mapping.inference.model,
        endpoint=inference_mapping.inference.endpoint,
    ), None


def list_configurations(db: Session, user_id: str):

    """
    Retrieves all configurations from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        Tuple: List of configuration responses and error message (if any).
    """

    configurations, is_error = repo.get_all_configurations(db, user_id)

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
            actions= [{
                "id": mapping.actions.id,
                "name": mapping.actions.name,
                "description": mapping.actions.description,
                "types": mapping.actions.types,
                "table": mapping.actions.table,
                "enable": mapping.actions.enable,
                } for mapping in capabilities.cap_actions_mapping],
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
        ) for inference_mapping in config.inference_mapping],
        vectordb=[VectorDBResponse(
            id= vector_db.vector_db.id,
            vectordb=vector_db.vector_db.vectordb,
            vectordb_config=vector_db.vector_db.vectordb_config,
            config_id=config.id,
        ) for vector_db in config.vectordb_config_mapping if vector_db.vector_db]
    ) for config in configurations]

    return config_list, None

def get_configuration(db: Session, config_id: int):
    """
    Retrieves a configuration by its ID.

    Args:
        db (Session): Database session dependency.
        config_id (int): ID of the configuration to retrieve.

    Returns:
        Tuple: Configuration response and error message (if any).
    """
    configuration, is_error = repo.get_configuration_by_id(config_id, db)

    if is_error:
        return configuration, "DB Error"

    if not configuration:
        return None, "Configuration not found"

    config_response = schemas.ConfigurationResponse(
        id=configuration.id,
        name=configuration.name,
        short_description=configuration.short_description,
        long_description=configuration.long_description,
        status=configuration.status,
        connector=[
            schemas.ConnectorResponse(
                connector_id=connector.connector.id,
                connector_type=connector.connector.connector_type,
                connector_name=connector.connector.connector_name,
                connector_description=connector.connector.connector_description,
                connector_config=connector.connector.connector_config,
                schema_config=connector.connector.schema_config,
                connector_docs=connector.connector.connector_docs,
                enable=connector.connector.enable
            ) for connector in configuration.connectors
        ],
        capabilities=[
            schemas.CapabilitiesBase(
                id=capabilities.id,
                name=capabilities.name,
                actions=[{
                    "id": mapping.actions.id,
                    "name": mapping.actions.name,
                    "description": mapping.actions.description,
                    "types": mapping.actions.types,
                    "table": mapping.actions.table,
                    "enable": mapping.actions.enable,
                } for mapping in capabilities.cap_actions_mapping],
                requirements=capabilities.requirements,
                description=capabilities.description,
                config_id=capabilities.config_id,
            ) for capabilities in configuration.capabilities
        ],
        inference=[
            schemas.InferenceResponse(
                id=inference_mapping.inference.id,
                name=inference_mapping.inference.name,
                apikey=inference_mapping.inference.apikey,
                llm_provider=inference_mapping.inference.llm_provider,
                model=inference_mapping.inference.model,
                endpoint=inference_mapping.inference.endpoint,
                config_id=inference_mapping.config_id
            ) for inference_mapping in configuration.inference_mapping
        ],
        vectordb=[
            VectorDBResponse(
                id=vector_db.vector_db.id,
                vectordb=vector_db.vector_db.vectordb,
                vectordb_config=vector_db.vector_db.vectordb_config,
                config_id=configuration.id,
            ) for vector_db in configuration.vectordb_config_mapping if vector_db.vector_db
        ]
    )

    return config_response, None

def delete_configuration(db: Session, config_id: int):
    """
    Deletes a configuration by its ID.

    Args:
        db (Session): Database session dependency.
        config_id (int): ID of the configuration to retrieve.

    Returns:
        Tuple: Configuration response and error message (if any).
    """
    configuration, is_error = repo.delete_configuration_by_id(config_id, db)

    if is_error:
        return configuration, "DB Error"

    if not configuration:
        return None, "Configuration not found"

    config_response = schemas.ConfigurationResponse(
        id=configuration.id,
        name=configuration.name,
        short_description=configuration.short_description,
        long_description=configuration.long_description,
        status=configuration.status,
        capabilities=[
            schemas.CapabilitiesBase(
                id=capabilities.id,
                name=capabilities.name,
                requirements=capabilities.requirements,
                description=capabilities.description,
                config_id=capabilities.config_id,
            ) for capabilities in configuration.capabilities
        ],
    )

    return config_response, None


def create_configuration(configuration: schemas.ConfigurationCreation, db: Session, user_id: str):

    """
    Creates a new configuration in the database.

    Args:
        configuration (ConfigurationCreation): The data for the new configuration.
        db (Session): Database session dependency.

    Returns:
        Tuple: Configuration response and error message (if any).
    """

    new_config, is_error = repo.create_new_configuration(configuration, db, user_id)
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

    """
    Updates an existing configuration based on its ID.

    Args:
        config_id (int): The ID of the configuration to update.
        configuration (ConfigurationUpdate): The updated data for the configuration.
        db (Session): Database session dependency.

    Returns:
        Tuple: Configuration response and error message (if any).
    """

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

    """
    Creates a new capability in the database.

    Args:
        capabilities (CapabilitiesBase): The data for the new capability.
        db (Session): Database session dependency.

    Returns:
        Tuple: Capability response and error message (if any).
    """

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

    """
    Retrieves all capabilities from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        Tuple: List of capability responses and error message (if any).
    """

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

    """
    Updates an existing capability based on its ID.

    Args:
        cap_id (int): The ID of the capability to update.
        capability (CapabilitiesUpdateBase): The updated data for the capability.
        db (Session): Database session dependency.

    Returns:
        Tuple: Capability response and error message (if any).
    """

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

    """
    Deletes a capability from the database based on its ID.

    Args:
        cap_id (int): The ID of the capability to delete.
        db (Session): Database session dependency.

    Returns:
        Tuple: Boolean indicating whether the deletion was successful and error message (if any).
    """

    deleted, is_error = repo.delete_capability(cap_id, db)

    if is_error:
        return deleted, "DB Error"

    if not deleted:
        return [], None

    return True, None


def update_datasource_documentations(db: Session, vector_store, datasources, id_name_mappings, config_id):
        logger.info("Updating datasource documentations")
        active_datsources = {}
        for key, datasource in datasources.items():
            connector_details = id_name_mappings.get(key, {})
            if "id" not in connector_details:
                logger.warning("Connector not found")
                continue

            logger.info(f"initialising datasource {key}")
            logger.info("mappings connector_details, id:{}".format(connector_details["id"]))

            datasource.connect()
            success, err = datasource.healthcheck()
            if not success:
                logger.error(f"Datasource health failed for {key}, cause: {err}")
                logger.warning(f"skipping datasource initialization for {key}")
                continue

            active_datsources[key] = datasource
            logger.info("Pushing plugin metadata to vector store")
            sd = SourceDocuments([], [], [])
            queries = []
            match datasource.__category__:
                case 1:
                    documentations = datasource.fetch_data()
                    sd = SourceDocuments([], [], documentations)
                case 2 | 5:
                    schema_config = connector_details.get("schema_config",[])
                    schema_details, metadata = datasource.fetch_schema_details()
                    sd = SourceDocuments(schema_details, schema_config, [])
                    queries = get_all_connector_samples(connector_details.get("id"), db)
                case 4:
                    documentations = datasource.fetch_data()
                    sd = SourceDocuments([], [], documentations)

            chunked_document, chunked_schema = sd.get_source_documents()
            vector_store.prepare_data(key, chunked_document,chunked_schema, queries, int(config_id))


        return active_datsources, None

def get_inference_and_plugin_configurations(db: Session, config_id: int):

    """
    Retrieves all inference and plugin configurations from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        Tuple: Configuration response and error message (if any).
    """

    configuration={}
    connectors, status = repo.get_connectors_by_configuration_id(config_id, db)
    if status:
        return configuration
    configs, is_error = repo.get_configuration_by_id(config_id, db)
    if configs is None:
        configuration["models"]=[]
    else:
        inference, is_error = create_inference_yaml(configs.id, db)
        configuration["models"] = inference

    datasources = []
    mappings  = {}

    for conn in connectors:
        provider, is_error = config_repo.get_provider_by_id(conn.connector_type, db)
        if is_error:
            continue
        datasource = formatting_datasource(conn, provider)
        if datasource:

            datasource['name'] = str(conn.connector_name).replace(" ", "_").lower()
            mappings[datasource['name']] = {
                "id": conn.id,
                "schema_config": conn.schema_config
            }
            datasource['description'] = conn.connector_description
            datasources.append(datasource)
    configuration["datasources"] = datasources
    configuration["mappings"] = mappings
    return configuration

def create_inference_yaml(config_id:int, db:Session):

    """
    Creates a YAML file for inference configurations based on the given configuration ID.

    Args:
        config_id (int): The ID of the configuration.
        db (Session): Database session dependency.

    Returns:
        Tuple: List of inference configurations and error message (if any).
    """

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

def get_all_connector_samples(connector_id: int, db: Session):
    sqls, is_error = provider_svc.getsqlbyconnector(connector_id, db)

    if is_error:
        logger.error(f"Error getting SQL from connector {connector_id}:{is_error}")


    queries = []
    for sql in sqls:
        queries.append({
                "description": sql.description,
                "metadata": sql.sql_metadata
            })
    return queries


def create_yaml_file(request:Request, config_id: int, db: Session):

    """
    Creates a YAML file for configurations based on the given configuration ID.

    Args:
        request (Request): Request object for logging purposes.
        config_id (int): The ID of the configuration.
        db (Session): Database session dependency.
    Returns:
    Tuple: Configuration YAML and error message (if any).

    """
    configuration, is_error = repo.get_configuration_by_id(config_id, db)
    if (configuration == [] or configuration==None) or is_error:
        return None, None, "Configuration Not Found"

    inferences, is_error = repo.get_inferences_by_config_id(config_id, db)
    if (inferences == [] or inferences==None) or is_error:
        return None, None, "Inference configuration not found"

    connectors, is_error = repo.get_connectors_by_configuration_id(config_id, db)
    if (connectors == [] or connectors==None) or is_error:
        return None, None, "Connector not found"

    datasources = []
    for conn in connectors:
        provider, is_error = config_repo.get_provider_by_id(conn.connector_type, db)
        if is_error:
            continue

        datasource = formatting_datasource(conn, provider)
        if datasource:
            datasource['name'] = str(conn.connector_name).replace(" ", "_").lower()
            datasource['description'] = conn.connector_description
            datasource['mappings'] =  {"id": conn.id, "schema_config":conn.schema_config}
            datasources.append(datasource)
            
    use_case = dict({
        'short_description': configuration.short_description,
        'long_description': configuration.long_description,
        'capabilities': [
                {
                "name": cap.name if cap.name else "default",
                "description": cap.description if cap.description else "No description provided",
                "requirements": cap.requirements if cap.requirements else [],
                "analysis": [],
                "action": [
                    {
                        "name": mapping.actions.name,
                        "description": mapping.actions.description,
                        "action": mapping.actions.types,
                        "table": mapping.actions.table,
                        "connector": {
                                "name": str(mapping.actions.connectors.connector_name).replace(" ", "_").lower(),
                        } if mapping.actions.connectors else None,
                        "body": mapping.actions.body,
                    } for mapping in cap.cap_actions_mapping
                ]
                } for cap in configuration.capabilities
         ]
    })
    
    if datasources is not None and use_case is not None:
        repo.update_configuration_status(config_id,db)
    return datasources, use_case, None



def formatting_datasource(connector, provider):

    """
    Formats the datasource based on the provider category.

    Args:
        connector (Connector): The connector object.
        provider (Provider): The provider object.

    Returns:
        dict: Formatted datasource or None if the provider category is not recognized.
    """

    if provider.category_id == 1:
        return {
            'type': provider.key,
            'params': connector.connector_config,
            'documentations': [{'type': 'text', 'value': connector.connector_docs}]
        }
    elif provider.category_id == 2 or provider.category_id == 5:
        return {
            'type': provider.key,
            'params': connector.connector_config,
            'documentations': [{'type': 'text', 'value': connector.connector_docs}]
        }
    elif provider.category_id == 3:
        return {
            'type': provider.key,
            'params': connector.connector_config,
            'documentations': []
        }
    elif provider.category_id == 4:
        return {
            'type': provider.key,
            'params': connector.connector_config
        }
    else:
        return None

def get_llm_provider_models(llm_provider: schemas.LLMProviderBase):
    """
    Retrieves the models available for a given LLM provider.
    Args:
        llm_provider (schemas.LLMProviderBase): The LLM provider object.
    Returns:
        Tuple: List of models and error message (if any).
    """
    if llm_provider.key:
        llm_provider.kind = llm_provider.key
        llm_provider.unique_name = llm_provider.key
        return BaseLoader(model_configs=[dict(llm_provider)]).load_model(unique_name=llm_provider.key).get_models()
    else:
        return None, "Missing LLM provider key"

def get_inference(inference_id: int, db: Session):

    """
    Retrieves an inference from the database based on its ID.

    Args:
        inference_id (int): The ID of the inference.
        db (Session): Database session dependency.

    Returns:
        Tuple: Inference response and error message (if any).
    """

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

    """
    Creates a new inference in the database.

    Args:
        inference (schemas.InferenceBase): The inference object to be created.
        db (Session): Database session dependency.

    Returns:
        Tuple: Inference response and error message (if any).
    """

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

    """
    Updates an inference in the database based on its ID.

    Args:
        inference_id (int): The ID of the inference to be updated.
        inference (schemas.InferenceBaseUpdate): The inference object with updated values.
        db (Session): Database session dependency.

    Returns:
        Tuple: Inference response and error message (if any).
    """

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

    """
    Retrieves all actions from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        Tuple: List of actions and error message (if any).
    """

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
            body = action.body,
            enable = action.enable,
            ) for action in actions], False

def get_actions(action_id:int, db:Session):

    """
    Retrieves an action from the database based on its ID.

    Args:
        action_id (int): The ID of the action.
        db (Session): Database session dependency.

    Returns:
        Tuple: Action response and error message (if any).
    """

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
        body = action.body,
    ), False

def get_actions_by_connector(connector_id:int, db:Session):

    """
    Retrieves all actions associated with a specific connector from the database.

    Args:
        connector_id (int): The ID of the connector.
        db (Session): Database session dependency.
    Returns:
        Tuple: List of actions and error message (if any).
    """

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
            body = action.body,
            ) for action in actions], False

def create_action(action: schemas.Actions, db:Session):

    """
    Creates a new action in the database.

    Args:
        action (schemas.Actions): The action object to be created.
        db (Session): Database session dependency.

    Returns:
        Tuple: Action response and error message (if any).
    """

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
        body = action.body,
    ), False


def update_action(action_id: int, action: schemas.ActionsUpdate, db: Session):

    """
    Updates an action in the database based on its ID.

    Args:
        action_id (int): The ID of the action to be updated.
        action (schemas.ActionsUpdate): The action object with updated values.
        db (Session): Database session dependency.

    Returns:
        Tuple: Action response and error message (if any).
    """

    updated_action, is_error = repo.update_action(action_id, action, db)

    if is_error:
        return updated_action, "DB Error"

    if updated_action is None:
        return [], None

    return schemas.ActionsResponse(
        id=updated_action.id,
        name=updated_action.name,
        description=updated_action.description,
        types=updated_action.types,
        condition=updated_action.condition,
        table = updated_action.table,
        connector_id=updated_action.connector_id,
        enable = updated_action.enable,
        body = updated_action.body,
    ), False


def delete_action(action_id: int, db: Session):

    """
    Deletes an action from the database based on its ID.

    Args:
        action_id (int): The ID of the action to be deleted.
        db (Session): Database session dependency.

    Returns:
        Tuple: Action response and error message (if any).
    """

    result, is_error = repo.delete_action_by_id(action_id, db)

    if is_error:
        return None, "DB Error"

    return result, False


def get_use_cases(db: Session):

    """
    Retrieves all use cases from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        Tuple: List of use cases and error message (if any).

    """

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
            actions = []
            for mapping in cap.cap_actions_mapping:
                temp = {
                        "name": mapping.actions.name,
                        "description": mapping.actions.description,
                        "action": mapping.actions.types,
                        "table": mapping.actions.table,
                        "body": mapping.actions.body,
                }
                if mapping.actions.connectors:
                    temp["connector"] = {
                        "name": str(mapping.actions.connectors.connector_name).replace(" ", "_").lower(),
                    }
                actions.append(temp)
                
            capability["action"] = actions
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

