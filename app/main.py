from typing import Union

from fastapi import FastAPI
from app.providers.container import Container
from app.api.v1.main_router import MainRouter
from app.api.v1.connector import router as ConnectorRouter
from app.api.v1.llmchat import chat_router
from app.api.v1.provider import router as ProviderRouter
from app.api.v1.connector import cap_router as capabilityrouter
from app.api.v1.connector import inference_router as inference_router
from app.api.v1.connector import actions as actions
from app.api.v1.provider import sample as sample_sql
import app.services.connector_details as commonservices


from fastapi.staticfiles import StaticFiles
from app.providers.data_preperation import SourceDocuments
from app.chain.chains.intent_chain import IntentChain
from app.chain.chains.capability_chain import CapabilityChain
from app.chain.chains.metadata_chain import MetadataChain
from app.chain.chains.chain import Chain
from app.providers.config import Configs, configs
from app.providers.context_storage import ContextStorage

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.utils.database import Base

from fastapi.middleware.cors import CORSMiddleware
from loguru import logger


import app.repository.connector as repo
import app.services.connector as svc
import app.services.provider as provider_svc

# from sqlalchemy.orm import Session
from app.utils.database import SessionLocal, Base, engine

session = SessionLocal()


def create_app(config):

    logger.info("creating application")
    logger.info("creating container object")
    container = Container()
    logger.info("loading necessery configurations")
    json_config =Configs().model_dump(mode='json') 
    container.config.from_dict(json_config)
    container.config.from_dict(config)

    config["models"] = []
    logger.level("ONEPANE", no=27, color="<yellow>")
    
    
    if container.config.logging_enabled():
        logger.add("trace.log", level="ONEPANE", colorize=False, backtrace=True, diagnose=True)
    
    logger.info("creating database tables")
    Base.metadata.create_all(bind=engine)
    

    logger.info("initializing vector store")
    vectore_store = container.vectorstore().load_class()
    vectore_store.connect()
    
    logger.info("initializing plugin providers")
    err = provider_svc.initialize_plugin_providers(session)
    if err is not None:
        logger.critical(err)

    err = commonservices.check_configurations_availability(session)
    datasources = []
    
    if err is None:
        logger.info("getting existing models and plugins configurations")
        configuration_yaml = svc.get_inference_and_plugin_configurations(session)
        
        logger.info("intializing datasource using container")
        container.config.from_dict(configuration_yaml)
        datasources = container.datasources()
        
        logger.info("setting datasources and inference details into configuration")
        config['datasources'] = configuration_yaml.get("datasources", [])
        config['models'] = configuration_yaml.get("models", [])
        config["use_case"] = svc.get_use_cases(session)   

        configs.inference_llm_model=config["models"][0]["unique_name"] if len(config["models"]) > 0 else None

        if len(config["datasources"]) >0:
            db_connectors, status = repo.get_all_connectors(session)
            if status:
                logger.error("db error", db_connectors)
            index = 0
            for key, datasource in datasources.items():
                logger.info(f"initialising datasource {key}")
                datasource.connect()
                success = datasource.healthcheck()
                if not success:
                    logger.warning("Datasource health failed")
                    continue
                
                logger.info("Pushing plugin metadata to vector store")
                schema_config = db_connectors[index].schema_config
                schema_details, metadata = datasource.fetch_schema_details()
                sd = SourceDocuments(schema_details, schema_config, [])
                chunked_document, chunked_schema = sd.get_source_documents()

                queries, is_error = provider_svc.get_quries_by_key(key, session)

                if is_error:
                    logger.error("error fetching queries", is_error)

                vectore_store.prepare_data(key,chunked_document,chunked_schema, queries)
                index += 1
    else:
        logger.warning(err)
        
    logger.info("creating local context storage")
    context_storage = ContextStorage(session)

    logger.info("initializing chain")
    genna_chain = Chain(config, vectore_store, datasources, context_storage)
    capability_chain = CapabilityChain(config, context_storage, genna_chain)
    metadata_chain = MetadataChain(config, vectore_store, datasources, context_storage)
    intent_chain = IntentChain(config, vectore_store, datasources, context_storage, genna_chain, capability_chain, metadata_chain)



    logger.info("creating llm fast_api server")
    app = FastAPI()

    app.mount("/assets",StaticFiles(directory="assets"), name="assets")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*',"localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info("setting chain, vector store into app context")
    app.config = config
    app.container = container
    app.vector_store = vectore_store    
    
    app.metadata_chain = metadata_chain
    app.chain = intent_chain
    app.context_storage = context_storage
    
    app.include_router(MainRouter,prefix="/api/v1/query")
    app.include_router(ConnectorRouter, prefix="/api/v1/connector")
    app.include_router(chat_router, prefix="/api/v1/chat")
    app.include_router(ProviderRouter, prefix="/api/v1/provider")
    app.include_router(capabilityrouter, prefix="/api/v1/capability")
    app.include_router(inference_router, prefix="/api/v1/inference")
    app.include_router(actions, prefix="/api/v1/actions")
    app.include_router(sample_sql, prefix="/api/v1/sql")


    curr_schema = app.openapi()
    curr_schema["info"]["title"] = "Onepane Chat API"
    curr_schema["info"]["description"] = "API for onepane cloud chatbot"



    return app
