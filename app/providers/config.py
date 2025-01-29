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
    auth_server: str = os.getenv("AUTH_SERVER", "localhost")
    username: str = os.getenv("ADMIN_USERNAME","admin")
    password: str = os.getenv("ADMIN_PASSWORD","password")
    secret_key: str = os.getenv("SECRET_KEY","secret")
    auth_enabled: bool = os.getenv("AUTH_ENABLED",True)
    default_username: str = os.getenv("DEFAULT_USERNAME", "Admin")
    credirect_url:str = os.getenv("OOAUTH_REDIRECT_URL","http://localhost:8001/api/v1/auth/callback")
    cclient_id:str = os.getenv('OOAUTH_CLIENT_ID','301994840332269984')
    cclient_secret:str = os.getenv('OOAUTH_CLIENT_SECRET','ViRi8h3QVHAQk3jNQQZFjR3gfn3Xh4ePcB4ThIdPHXFldMNXsOrNStmouiOjZ04F')
    cauthorization_url:str = os.getenv('OOAUTH_AUTHORIZATION_URL','https://flask-auth-pogve2.us1.zitadel.cloud/oauth/v2/authorize')
    ctoken_url:str = os.getenv('OOTOKEN_URL','https://flask-auth-pogve2.us1.zitadel.cloud/oauth/v2/token')
    ctoken_userinfo_url:str= os.getenv('OOUSERINFO','https://flask-auth-pogve2.us1.zitadel.cloud/oidc/v1/userinfo')
    cclient_id_test_api:str=os.getenv('TEST_API','302875443080538159')
    cintrospection_url:str = os.getenv('OINTROSPECTION','https://flask-auth-pogve2.us1.zitadel.cloud/oauth/v2/introspect')
    cfrontend_uri:str  = os.getenv('FRONTEND_CALLBACK_URI','http://localhost:5000')



    retry_limit:int = os.getenv("RETRY_LIMIT",0)
    application_port: int = os.getenv("APP_PORT", 8001)


configs = Configs()
