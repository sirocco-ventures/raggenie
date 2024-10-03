import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Configs(BaseSettings):
    # base
    ENV: str = os.getenv("ENV", "dev")
    API: str = "/api"
    PROJECT_NAME: str = "raggenie"

    DATABASE_URL: str = "sqlite:///raggenie.db"

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # database
    logging_enabled: bool = os.getenv("ENABLE_FILE_LOGGING", False)
    inference_llm_model:str = os.getenv("INFERENCE_LLM_MODEL", "gpt")

    # Auth
    AUTH_SERVER: str = os.getenv("AUTH_SERVER", "localhost")
    USERNAME: str = os.getenv("USERNAME","admin")
    PASSWORD: str = os.getenv("PASSWORD","password")
    SECRET_KEY: str = os.getenv("SECRET_KEY","secret")
    LOGIN_SERVER: str = os.getenv("LOGIN_SERVER","test")

    retry_limit:int = os.getenv("RETRY_LIMIT",0)
    application_port: int = os.getenv("APP_PORT", 8001)


configs = Configs()
