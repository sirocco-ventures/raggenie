from sqlalchemy.orm import Session
import app.repository.provider as repo
import app.schemas.provider as schemas
from app.services.connector_details import test_plugin_connection
from app.providers.container import Container
from app.repository import connector as conn_repo
import json
from fastapi import Request
from app.utils.module_reader import get_plugin_providers
from app.models.provider import Provider, ProviderConfig
from loguru import logger
from app.utils.module_reader import get_llm_providers

class PuginsHandler():

    def __init__(self) -> None:
        pass


def initialize_plugin_providers(db:Session):
    providers = get_plugin_providers()

    for i in providers:

        data, is_error = repo.insertorUpdateData(db,Provider,{"key":i['plugin_name']},{
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
                confdata, is_error = repo.insertorUpdateData(db,ProviderConfig, {"provider_id":data.id,"slug":conf.slug},{
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
    provider, is_error = repo.get_provider_by_id(provider_id, db)
    if provider is None or is_error:
        return provider, "Provider Not Found"

    provider_configs, is_error = repo.get_config_types(provider_id, db)
    if is_error:
        return provider_configs, "Failed to get provider configurations"

    match provider.category_id:
        case 2:
            return test_plugin_connection(provider_configs, config, provider.key)
        case _:
            return None, "Unsupported Provider"
        

def getllmproviders(request: Request):
    
    providers = get_llm_providers()

    return {"providers": providers}, None
    
def getsqlbyconnector(id:int, db:Session):
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

    sql, is_error =  repo.create_sql(sql,db)

    if is_error:
        return sql, "DB Error"
    if not sql:
        return [], None

    insertVectorStore(request, sql, db)

    return schemas.SampleSQLResponse(
        description=sql.description,
        sql_metadata=sql.sql_metadata,
        connector_id=sql.connector_id,
        id= sql.id,
    ), False

def update_sql(request: Request, sql_id: int, sql: schemas.SampleSQLUpdate, db: Session):
    sql, is_error = repo.update_sql(sql_id, sql, db)

    if is_error:
        return sql, "DB Error"

    if not sql:
        return {}, None
    
    insertVectorStore(request, sql, db)

    return schemas.SampleSQLResponse(
        description=sql.description,
        sql_metadata=sql.sql_metadata,
        connector_id=sql.connector_id,
        id= sql.id,
    ), False

def delete_sql(sql_id: int, db: Session):
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

def insertVectorStore(request, sql, db: Session):
    datasource, is_error = conn_repo.get_connector_by_id(sql.connector_id, db)

    vectore_store = request.app.vector_store
    vectore_store.connect()
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
