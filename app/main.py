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
from app.api.v1.auth import login as login
import app.services.connector_details as commonservices


# from app.providers.middleware import AuthMiddleware
from fastapi.staticfiles import StaticFiles
from app.chain.chains.intent_chain import IntentChain
from app.chain.chains.capability_chain import CapabilityChain
from app.chain.chains.metadata_chain import MetadataChain
from app.chain.chains.query_chain import QueryChain
from app.chain.chains.general_chain import GeneralChain
from app.providers.config import Configs, configs
from app.providers.context_storage import ContextStorage

from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import app.services.connector as svc
import app.services.provider as provider_svc
from app.utils.database import SessionLocal, Base, engine

session = SessionLocal()


def create_app(config):

    logger.info("creating application")
    logger.info("creating container object")
    container = Container()
    logger.info("loading necessary configurations")
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
        logger.info("checking execution mode")

        logger.info("getting existing models and plugins configurations")
        configuration_yaml = svc.get_inference_and_plugin_configurations(session)

        logger.info("initializing datasource using container")
        container.config.from_dict(configuration_yaml)
        datasources = container.datasources()

        logger.info("setting datasources and inference details into configuration")
        config['datasources'] = configuration_yaml.get("datasources", [])
        config['models'] = configuration_yaml.get("models", [])
        id_name_mappings = configuration_yaml.get("mappings", {})
        config["use_case"] = svc.get_use_cases(session)


        configs.inference_llm_model=config["models"][0]["unique_name"] if len(config["models"]) > 0 else None

        if len(config["datasources"]) >0:
            datasources, err = svc.update_datasource_documentations(session, vectore_store, datasources, id_name_mappings)
            if err is not None:
                logger.error("Error loading data into vector store")


    logger.info("creating local context storage")
    context_storage = ContextStorage(session)

    logger.info("initializing chain")
    query_chain = QueryChain(config, vectore_store, datasources, context_storage)
    general_chain = GeneralChain(config, vectore_store, datasources, context_storage)
    capability_chain = CapabilityChain(config, context_storage, query_chain)
    metadata_chain = MetadataChain(config, vectore_store, datasources, context_storage)
    intent_chain = IntentChain(config, vectore_store, datasources, context_storage, query_chain, general_chain, capability_chain, metadata_chain)



    logger.info("creating llm fast_api server")
    app = FastAPI()

    app.mount("/assets",StaticFiles(directory="assets"), name="assets")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5000"],
        allow_credentials=True,
        allow_methods=["OPTIONS", "GET", "POST"],
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
    app.include_router(login, prefix="/api/v1/auth")

    curr_schema = app.openapi()
    curr_schema["info"]["title"] = "Rag genie Chat API"
    curr_schema["info"]["description"] = "API for raggenie cloud chatbot"

    return app
