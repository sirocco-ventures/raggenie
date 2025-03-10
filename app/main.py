from fastapi import FastAPI
from app.providers.container import Container
from app.api.v1.main_router import MainRouter
from app.api.v1.connector import router as ConnectorRouter
from app.api.v1.llmchat import chat_router
from app.api.v1.provider import router as ProviderRouter
from app.api.v1.provider import vectordb as vectordb
from app.api.v1.connector import cap_router as capabilityrouter
from app.api.v1.connector import inference_router as inference_router
from app.api.v1.connector import actions as actions
from app.api.v1.provider import sample as sample_sql
from app.api.v1.auth import login as login
import app.services.connector_details as commonservices

from fastapi.responses import HTMLResponse


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

from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional

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


    logger.info("initializing plugin providers")
    err = provider_svc.initialize_plugin_providers(session)
    if err is not None:
        logger.critical(err)

    logger.info("initializing vector store")
    err = provider_svc.initialize_vectordb_provider(session)
    if err is not None:
        logger.critical(err)

    logger.info("initializing Vector Embeddings")
    err = provider_svc.initialize_embeddings(session)
    if err is not None:
        logger.critical(err)


    logger.info("creating local context storage")
    context_storage = ContextStorage(session)

    
    logger.info("creating llm fast_api server")
    app = FastAPI()

    app.mount("/assets",StaticFiles(directory="./assets"), name="assets")
    app.mount("/ui/assets",StaticFiles(directory="./ui/dist/assets",  html=True), name="ui", )

    templates = Jinja2Templates(directory="./ui/dist")

    @app.get("/ui", response_class=HTMLResponse)
    @app.get("/ui/{full_path:path}", response_class=HTMLResponse)
    def serve_home(request: Request, full_path: Optional[str]=""):
        if request:
            return templates.TemplateResponse("index.html", context= {"request": request}) 
        else:
            return templates.TemplateResponse("index.html") 

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["OPTIONS", "GET", "POST", "DELETE"],
        allow_headers=["*"],
    )

    logger.info("setting chain, vector store into app context")
    app.config = config
    app.container = container
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
    app.include_router(vectordb, prefix="/api/v1/vectordb")

    curr_schema = app.openapi()
    curr_schema["info"]["title"] = "Rag genie Chat API"
    curr_schema["info"]["description"] = "API for raggenie cloud chatbot"

    return app
