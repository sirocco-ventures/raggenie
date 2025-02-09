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
    
    zitadel_cctoken: str = os.getenv("ZITADEL_CCTOKEN", "eyJhbGciOiJSUzI1NiIsImtpZCI6IjMwNjM3MjQyNzMzMDM1NTIwMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAiLCJzdWIiOiIzMDU4OTgyOTQ5MDE0NzMyODMiLCJhdWQiOlsiMzA0NDUyNDgwMzQ1OTY0NTQ3Il0sImV4cCI6MTczOTE1MTM5NiwiaWF0IjoxNzM5MTA4MTk3LCJuYmYiOjE3MzkxMDgxOTcsImNsaWVudF9pZCI6InJhZ2dlbmllLWJhY2tlbmQiLCJqdGkiOiJWMl8zMDYzNzI0MjY1NTg2MDMyNjYtYXRfMzA2MzcyNDI2NTU4NjY4ODAyIn0.LY_fj43K8JcdScmlbMYFFUgKdy4HSGu9R9uXmcsgZI1nmJOQ5w1v5DdvWVv629C0CTQvMqAyHWc6zgl1_6sn2sW_p0rCWV-hIzcZTnjF9qaXkvxLMR6EpJ5wb0QuXMHg7mbZrrtr5lP7zxy3at-6lhw04bv65fdV1Dy-sNtSAg2WtdSny-cpqhsbrL9jEKYVS0wtSEdXJZjRvTlf8BRArDKVpCO3ui8fgHBzXqqjE56tUs5mTGeh2WospMgKc1hWULOPwWOOooJ6LoQCW7pkFQqYWYvEw7dihl4DHQ8gO6Et7KyhMDev6T2gXGT1tUT03jQSZYE1-hA13AX_zUVETQ")
    zitadel_domain: str = os.getenv("ZITADEL_DOMAIN", "http://localhost:8080")
    retry_limit:int = os.getenv("RETRY_LIMIT",0)
    application_port: int = os.getenv("APP_PORT", 8001)
    


configs = Configs()
