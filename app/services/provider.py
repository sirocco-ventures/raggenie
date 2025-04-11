from sqlalchemy.orm import Session
import app.repository.provider as repo
import app.schemas.provider as schemas
import app.schemas.connector as conn_schemas
from app.services.connector_details import test_plugin_connection, test_vector_db_credentials
from app.loaders.base_loader import BaseLoader
from app.repository import connector as conn_repo
from fastapi import Request
from app.utils.module_reader import get_plugin_providers, get_vectordb_providers
from app.models.provider import Provider, ProviderConfig, VectorDBConfig
from loguru import logger
from app.utils.module_reader import get_llm_providers, get_all_embedding
from app.vectordb.loader import VectorDBLoader
from app.embeddings.loader import EmLoader

def test_inference_credentials(inference: conn_schemas.InferenceBase):
    """
    Tests the connection credentials for a specific LLM inference based on its provider.

    Args:
        inference (conn_schemas.InferenceBase):
            A configuration object containing the provider details for testing the credentials.

    Returns:
        Tuple[bool, str]:
            - (True, "Test Credentials successfully completed") if the credentials are valid and the test is successful.
            - (None, error_message) if there was an error during the test or inference.
            - (False, "Unsupported Inference") if the LLM provider is not recognized or unsupported.
    """

    model_configs = [{
        "unique_name": inference.name,
        "name": inference.model,
        "api_key": inference.apikey,
        "endpoint": inference.endpoint,
        "kind" : inference.llm_provider,
    }]

    try:
        inference_model = BaseLoader(model_configs= model_configs).load_model(inference.name)
    except Exception as error:
        return None, str(error)

    output, response_metadata = inference_model.do_inference(
            "hi", []
    )
    if output['error'] is not None:
        return None, output['error']
    return True, "Test Credentials successfully completed"

def initialize_vectordb_provider(db:Session):
    """
    Initializes the vector database by fetching the vector database data and inserting or updating
    their details in the database.

    Args:
        db (Session): Database session used for performing transactions.
    """

    vector_dbs = get_vectordb_providers()

    for i in vector_dbs:
        data, is_error = repo.insert_or_update_data(db,VectorDBConfig, {"key":i['vectordb_name']},{
            "name":i["display_name"],
            "description":i["description"],
            "icon":i["icon"],
            "key":i["vectordb_name"],
            "config": i["config"] if i["config"] is not None else None
        })

        if is_error:
            logger.error(f"Error inserting {i['vectordb_name']} {data}")

def initialize_embeddings(db:Session):
    pass


def initialize_plugin_providers(db:Session):

    """
    Initializes the plugin providers by fetching the plugin provider data and inserting or updating
    their details in the database. It also updates the provider configuration for each plugin.

    Args:
        db (Session): Database session used for performing transactions.
    """

    providers = get_plugin_providers()

    for i in providers:

        data, is_error = repo.insert_or_update_data(db,Provider,{"key":i['plugin_name']},{
            "name":i["display_name"],
            "description":i["description"],
            "icon":i["icon"],
            "category_id":i["category"],
            "key":i["plugin_name"],
            "actions_enabled": i["actions_enabled"],
            "actions_supported": i["actions_supported"],
        })

        if is_error:
            logger.error(f"Error inserting {i['plugin_name']} {data}")
        else:

            for conf in i["args"].values():
                confdata, is_error = repo.insert_or_update_data(db,ProviderConfig, {"provider_id":data.id,"slug":conf.slug},{
                    "provider_id":data.id,
                    "name":conf.generic_name,
                    "description":conf.description,
                    "field":conf.slug,
                    "slug":conf.slug,
                    "value":conf.value,
                    "order":conf.order,
                    "required":conf.required,
                    "config_type":conf.type
                })
                if is_error:
                    logger.error("Error inserting", conf.name, confdata)



def list_providers(db: Session):

    """
    Lists all available providers from the database and returns their details along with configurations.

    Args:
        db (Session): Database session used for performing transactions.

    Returns:
        (List[schemas.ProviderResp], str | None): List of provider details or an error message.
    """

    providers, is_error = repo.get_all_providers(db)

    if is_error:
        return providers, "DB Error"

    if not providers:
        return [],None

    provider_list = [
        schemas.ProviderResp(
            id=provider.id,
            name=provider.name,
            description=provider.description,
            enable=provider.enable,
            icon=provider.icon,
            category_id=provider.category_id,
            key = provider.key,
            actions_supported= provider.actions_supported,
            actions_enabled = provider.actions_enabled,
            configs=[
                {
                    'id': config.id,
                    'name': config.name,
                    'description': config.description,
                    'field': config.field,
                    'slug': config.slug,
                    'provider_id': config.provider_id,
                    'config_type': config.config_type,
                    'order': config.order,
                    'required':config.required,
                    'value':config.value
                }
                for config in provider.providerconfig
            ]
        )
        for provider in providers
    ]

    return provider_list, None

def get_provider(provider_id: int,db: Session):

    """
    Retrieves the details of a specific provider by its ID.

    Args:
        provider_id (int): The unique identifier of the provider.
        db (Session): Database session used for performing transactions.

    Returns:
        (schemas.ProviderResp, str | None): The provider details or an error message.
    """

    provider, is_error = repo.get_provider_by_id(provider_id,db)

    if is_error:
        return provider, "DB Error"

    if not provider:
        return {}, None

    provider_data = {
        'id': provider.id,
        'name': provider.name,
        'description': provider.description,
        'enable': provider.enable,
        'icon': provider.icon,
        'category_id': provider.category_id,
        'key': provider.key,
        'actions_enabled': provider.actions_enabled,
        'actions_supported': provider.actions_supported,
        'configs': [
            {
                'id': config.id,
                'name': config.name,
                'description': config.description,
                'field': config.field,
                'slug': config.slug,
                'provider_id': config.provider_id,
                'config_type': config.config_type,
                'order': config.order,
                'required':config.required,
                'value':config.value
            }
            for config in provider.providerconfig
        ]
    }

    provider_resp = schemas.ProviderResp(**provider_data)

    return provider_resp, None

def test_vectordb_credentials(config:schemas.TestVectorDBCredentials, db:Session):
    """
    Tests the credentials of a specific vector database based on its configuration.

    Args:
        config (schemas.TestVectorDBCredentials): Credentials to test.
        db (Session): Database session used for performing transactions.

    Returns:
        (str, str | None): A success message or an error message if unsupported.
    """
    db_config, is_error = repo.get_vector_db_config(db, config.vectordb_config["key"])

    if is_error:
        return None, db_config

    # if config.embedding_config:
    #     config.embedding_config["vectordb"] = config.vectordb_config["key"]


    return vector_embedding_connector(config, db_config)

def vector_embedding_connector(config, db_config):

    # if config.embedding_config:
    #     err = EmLoader(config.embedding_config).load_embclass().health_check()
    #     if err:
    #         return err, False

    match config.vectordb_config["key"]:
        case ("chroma" | "mongodb"):
            return test_vector_db_credentials(db_config,config, config.vectordb_config["key"])
        case _:
            return None, "Unsupported Vector Database Provider"




def test_credentials(provider_id: int, config: schemas.TestCredentials, db: Session):

    """
    Tests the credentials of a specific provider based on its configuration.

    Args:
        provider_id (int): The unique identifier of the provider.
        config (schemas.TestCredentials): Credentials to test.
        db (Session): Database session used for performing transactions.

    Returns:
        (str, str | None): A success message or an error message if unsupported.
    """

    provider, is_error = repo.get_provider_by_id(provider_id, db)
    if provider is None or is_error:
        return provider, "Provider Not Found"

    provider_configs, is_error = repo.get_config_types(provider_id, db)
    if is_error:
        return provider_configs, "Failed to get provider configurations"

    match provider.category_id:
        case 1:
            return test_plugin_connection(provider_configs, config, provider.key)
        case 2:
            return test_plugin_connection(provider_configs, config, provider.key)
        case 3:
            return test_plugin_connection(provider_configs, config, provider.key)
        case 4:
            return test_plugin_connection(provider_configs, config, provider.key)
        case 5:
            return test_plugin_connection(provider_configs, config, provider.key)
        case _:
            return None, "Unsupported Provider"

def getvectordbs(db: Session):
    """
    Returns a list of available vector databases.

    Args:
        request (Request): Request object used for handling incoming requests.

    Returns:
        dict: List of available vector databases.
    """

    vector_dbs,is_error = repo.get_vectordb_providers(db)

    if is_error:
        return vector_dbs, "DB Error"

    if not vector_dbs:
        return [], None

    resp = [
        schemas.VectorDBConfigResponse(
            id=db.id,
            name=db.name,
            description=db.description,
            icon=db.icon,
            key=db.key,
            config=db.config if db.config is not None else [],
        ) for db in vector_dbs
    ]

    return resp, None

def getllmproviders(request: Request):

    """
    Returns a list of available LLM providers.

    Args:
        request (Request): Request object used for handling incoming requests.

    Returns:
        dict: List of available LLM providers.
    """

    providers = get_llm_providers()

    return {"providers": providers}, None

def getsqlbyconnector(id:int, db:Session):

    """
    Retrieves SQL metadata based on a connector ID.

    Args:
        id (int): The unique identifier of the connector.
        db (Session): Database session used for performing transactions.

    Returns:
        (List[schemas.SampleSQLResponse], str | None): List of SQL metadata or an error message.
    """

    sqls, is_error = repo.get_sql_by_connector(id, db)


    if is_error:
        return sqls, "DB Error"

    if not sqls:
        return [], None

    sql_list = [
        schemas.SampleSQLResponse(
            id=sql.id,
            description=sql.description,
            sql_metadata=sql.sql_metadata,
            connector_id=sql.connector_id,
        )
        for sql in sqls
    ]

    return sql_list, None
def listsql(db:Session, user_id: str):

    """
    Retrieves a list of SQL samples from the database.

    Args:
        db (Session): Database session object.

    Returns:
        Tuple: List of SampleSQLResponse schemas and error message (if any).
    """

    sqls, is_error = repo.list_sql(db, user_id)

    if is_error:
        return sqls, "DB Error"

    if not sqls:
        return [], None

    sql_list = [
        schemas.SampleSQLResponse(
            id=sql.id,
            description=sql.description,
            sql_metadata=sql.sql_metadata,
            connector_id=sql.connector_id,
        )
        for sql in sqls
    ]

    return sql_list, None

def getsql(id:int, db:Session):

    """
    Retrieves a specific SQL sample by its ID from the database.

    Args:
        id (int): ID of the SQL sample to retrieve.
        db (Session): Database session object.

    Returns:
        Tuple: SampleSQLResponse schema and error message (if any).
    """

    sqls, is_error = repo.get_sql(id,db)

    if is_error:
        return sqls, "DB Error"

    if not sqls:
        return {}, None

    sql_data = {
        'id': sqls.id,
        'description': sqls.description,
       'sql_metadata': sqls.sql_metadata,
        'connector_id': sqls.connector_id,
    }

    sql_resp = schemas.SampleSQLResponse(**sql_data)

    return sql_resp, None

def create_sql(request: Request,sql:schemas.SampleSQLBase,db:Session, user_id: str):

    """
    Creates a new SQL sample in the database and updates the vector store.

    Args:
        request (Request): Request object to access app components.
        sql (schemas.SampleSQLBase): Data for the new SQL sample.
        db (Session): Database session object.

    Returns:
        Tuple: SampleSQLResponse schema and error message (if any).
    """

    sql, is_error =  repo.create_sql(sql,db,user_id)

    if is_error:
        return sql, "DB Error"
    if not sql:
        return [], None

    insert_vector_store(request, sql, db)

    return schemas.SampleSQLResponse(
        description=sql.description,
        sql_metadata=sql.sql_metadata,
        connector_id=sql.connector_id,
        id= sql.id,
    ), False

def update_sql(request: Request, sql_id: int, sql: schemas.SampleSQLUpdate, db: Session):

    """
    Updates an existing SQL sample in the database and updates the vector store.

    Args:
        request (Request): Request object to access app components.
        sql_id (int): ID of the SQL sample to update.
        sql (schemas.SampleSQLUpdate): Updated data for the SQL sample.
        db (Session): Database session object.

    Returns:
        Tuple: SampleSQLResponse schema and error message (if any).
    """

    sql, is_error = repo.update_sql(sql_id, sql, db)

    if is_error:
        return sql, "DB Error"

    if not sql:
        return {}, None

    insert_vector_store(request, sql, db)

    return schemas.SampleSQLResponse(
        description=sql.description,
        sql_metadata=sql.sql_metadata,
        connector_id=sql.connector_id,
        id= sql.id,
    ), False

def delete_sql(sql_id: int, db: Session):

    """
    Deletes an SQL sample by its ID from the database.

    Args:
        sql_id (int): ID of the SQL sample to delete.
        db (Session): Database session object.

    Returns:
        Tuple: SampleSQLResponse schema and error message (if any).
    """

    sql, is_error = repo.delete_sql(sql_id, db)

    if is_error:
        return sql, "DB Error"

    if not sql:
        return {}, None

    return schemas.SampleSQLResponse(
        description=sql.description,
        sql_metadata=sql.sql_metadata,
        connector_id=sql.connector_id,
        id=sql.id,
    ), False

def get_quries_by_key(key:str, db: Session):

    """
    Retrieves SQL samples based on a specific key.

    Args:
        key (str): Key to filter SQL samples (Connector Name).
        db (Session): Database session object.

    Returns:
        Tuple: List of dictionaries containing SQL descriptions and metadata, and error message (if any).
    """

    sql, is_error = repo.get_sql_by_key(key, db)
    if is_error:
        return sql, "DB Error"

    if not sql:
        return {}, None

    return [
        {
            "description": sql.description,
            "metadata": sql.sql_metadata
        }
    ], None

def insert_vector_store(request, sql, db: Session):

    """
    Inserts SQL data into the vector store.

    Args:
        request (Request): Request object to access app components.
        sql: SQL sample data to be inserted.
        db (Session): Database session object.

    Returns:
        str: Error message if an exception occurs, otherwise None.
    """

    datasource, is_error = conn_repo.get_connector_by_id(sql.connector_id, db)

    vectore_store = request.app.vector_store
    queries = [
        {
            "description": sql.description,
            "metadata": sql.sql_metadata
        }
    ]

    try :
        vectore_store.prepare_data(datasource_name=datasource.connector_name, queries=queries, chunked_document = None, chunked_schema = None)
    except Exception as e:

        return str(e)

def create_vector_db_default_config(vectordb):
    if vectordb.embedding_config is None:
        vectordb.embedding_config = {"provider": "default", "params": {}}

    if not vectordb.vectordb:
        vectordb.vectordb = "chroma"
        vectordb.vectordb_config = {"path": "./vector_db"}

    return vectordb

def attach_vector_config_if_missing(vectordb, db):

    inference, is_error = conn_repo.get_inference_by_config(vectordb.config_id, db)

    if is_error:
        return "Inference not found", is_error

    if vectordb.embedding_config.get("provider") == inference.llm_provider and not vectordb.embedding_config["params"].get("api_key"):
        vectordb.embedding_config["params"]["api_key"] = inference.apikey

    return vectordb, None


def create_vectordb_and_embedding(key,id,vectordb, db):

    """
    Creates a new VectorDB instance and inserts an embedding into the vector store.

    Args:
        vectordb (schemas.VectorDB): VectorDB instance data.
        db (Session): Database session object.

    Returns:
        Tuple: VectorDBResponse schema and error message (if any).
    """

    vectordb = create_vector_db_default_config(vectordb)

    vectordb, is_error = attach_vector_config_if_missing(vectordb, db)

    if is_error:
        return vectordb, is_error

    db_data, is_error = repo.create_vectordb_with_embedding(key,id, vectordb, db)

    if is_error:
        return vectordb, "DB Error"

    response_data = {
        'id': db_data['vectordb'].id,
        'vectordb': db_data['vectordb'].vectordb,
        'vectordb_config': db_data['vectordb'].vectordb_config,
        'config_id': db_data['vectordb_mapping'].config_id,
    }

    return schemas.VectorDBResponse(**response_data), None


def get_vectordb_instance(id: int, db: Session):
    """
    Retrieves a VectorDB instance by its ID.

    Args:
        id (int): The ID of the VectorDB instance.
        db (Session): Database session object.

    Returns:
        Tuple: VectorDBResponse schema and error message (if any).
    """

    (vectordb_instance, embedding), is_error = repo.get_vectordb_instance(id, db)

    if is_error:
        return vectordb_instance, "DB Error"


    return schemas.VectorDBResponse(
        id=vectordb_instance.id,
        vectordb=vectordb_instance.vectordb,
        vectordb_config=vectordb_instance.vectordb_config,
        config_id=vectordb_instance.vectordb_config_mapping[0].config_id,
        embedding_config={"provider": embedding.provider,"config": embedding.config}
    ), None

def delete_vectordb_instance(id: int, db: Session):
    """
    Deletes a VectorDB instance and its associated config mapping by ID.

    Args:
        id (int): The ID of the VectorDB instance to delete.
        db (Session): Database session object.

    Returns:
        Tuple: Success message and error message (if any).
    """

    success, is_error = repo.revoke_existing_vectordb_confg(id, db)

    if is_error:
        return success, "DB Error or VectorDB not found"

    return success, None

def create_vectorstore_instance(db:Session, config_id: int):
    """
    Creates a new vector store instance.

    Args:
        db (Session): Database session object.

    Returns:
        Tuple: VectorStoreConfigResponse schema and error message (if any).
    """
    configs, is_error = conn_repo.get_configuration_by_id(config_id, db)
    vector_store_formatting=None
    vectore_store = None

    if is_error:
        return configs, "DB Error"

    if configs:

        vectore_store, is_error = repo.get_mapped_vector_store(db, configs.id)

    if vectore_store:
        vector_store_formatting = {
            "name": vectore_store.get("vectordb"),
            "params": {**vectore_store.get("vectordb_config", {})}
        }


        vectordb_config = vectore_store.get("vectordb_config", {})

        if vectordb_config:
            embeddings = vectore_store.get("embedding_config", {})

            vector_store_formatting["embeddings"] = {
                **embeddings,
                "provider": vectore_store.get("em_provider"),
                "vectordb": vectore_store.get("vectordb")
            }

            vector_store_formatting={**vector_store_formatting,**vectordb_config}

    vectorloader = VectorDBLoader(vector_store_formatting) if vector_store_formatting else VectorDBLoader(config={"name":"chroma", "params":{"path":"./chromadb"}})

    return vectorloader.load_class(), None


def get_all_embeddings():

    """
    Returns a list of available LLM providers.

    Args:
        request (Request): Request object used for handling incoming requests.

    Returns:
        dict: List of available LLM providers.
    """

    embeddings = get_all_embedding()

    return embeddings, None