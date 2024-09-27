from sqlalchemy.orm import Session
import app.repository.provider as repo
import app.schemas.provider as schemas
from app.services.connector_details import test_plugin_connection
from app.loaders.base_loader import BaseLoader
from app.repository import connector as conn_repo
from fastapi import Request
from app.utils.module_reader import get_plugin_providers
from app.models.provider import Provider, ProviderConfig
from loguru import logger
from app.utils.module_reader import get_llm_providers

def test_inference_credentials(config: schemas.TestCredentials):

    """
    Tests the connection credentials for a specific LLM inference based on its provider.

    Args:
        config (schemas.TestCredentials): Configuration object containing the provider details for testing the credentials.

    Returns:
        (bool, str): 
            - True if the test credentials are successfully completed.
            - "Unsupported Inference" if the LLM provider is not recognized.
            - None and an error message if there was an error during inference.
    """
    provider_config = config.provider_config
    model_configs = [{
        "unique_name": provider_config["name"],
        "name": provider_config["model"],
        "api_key": provider_config["apikey"],
        "endpoint": provider_config["endpoint"],
        "kind" : provider_config["llm_provider"],
    }]
    inference_model = BaseLoader(model_configs= model_configs).load_model(provider_config["name"])
    output, response_metadata = inference_model.do_inference(
            "hi", []
    )
    if "error" in output:
        return None, output['error']
    return True, "Test Credentials successfully completed"


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
            "key":i["plugin_name"]
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
        case _:
            return None, "Unsupported Provider"


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
def listsql(db:Session):

    """
    Retrieves a list of SQL samples from the database.

    Args:
        db (Session): Database session object.

    Returns:
        Tuple: List of SampleSQLResponse schemas and error message (if any).
    """

    sqls, is_error = repo.list_sql(db)

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

def create_sql(request: Request,sql:schemas.SampleSQLBase,db:Session):

    """
    Creates a new SQL sample in the database and updates the vector store.

    Args:
        request (Request): Request object to access app components.
        sql (schemas.SampleSQLBase): Data for the new SQL sample.
        db (Session): Database session object.

    Returns:
        Tuple: SampleSQLResponse schema and error message (if any).
    """

    sql, is_error =  repo.create_sql(sql,db)

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
