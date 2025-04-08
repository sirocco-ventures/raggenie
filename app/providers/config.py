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
    auth_server: str = os.getenv("AUTH_SERVER", "0.0.0.0")
    username: str = os.getenv("ADMIN_USERNAME","admin")
    password: str = os.getenv("ADMIN_PASSWORD","password")
    secret_key: str = os.getenv("SECRET_KEY","secret")
    auth_enabled: bool = os.getenv("AUTH_ENABLED",True)
    default_username: str = os.getenv("DEFAULT_USERNAME", "Admin")
    
    client_private_key_file_path: str = os.getenv("CLIENT_PRIVATE_KEY_FILE_PATH", "app/providers/client-key-file.json")
    zitadel_token_url: str = os.getenv("ZITADEL_TOKEN_URL", "http://localhost:8080/oauth/v2/token")
    zitadel_domain: str = os.getenv("ZITADEL_DOMAIN", "http://localhost:8080")
    retry_limit:int = os.getenv("RETRY_LIMIT",0)
    application_port: int = os.getenv("APP_PORT", 8001)
    
    # Cache
    config_cache_limit: int = os.getenv("CONFIG_CACHE_LIMIT", 10)
    

    indexing_enabled: bool = os.getenv("INDEXING", False)



configs = Configs()
