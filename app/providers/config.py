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
    auth_enabled: bool = os.getenv("AUTH_ENABLED",False)
    default_username: str = os.getenv("DEFAULT_USERNAME", "Admin")
    
    zitadel_cctoken: str = os.getenv("ZITADEL_CCTOKEN", "eyJhbGciOiJSUzI1NiIsImtpZCI6IjMwNjAyOTI2OTg0NTI3ODcyMyIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAiLCJzdWIiOiIzMDU4OTgyOTQ5MDE0NzMyODMiLCJhdWQiOlsiMzA0NDUyNDgwMzQ1OTY0NTQ3Il0sImV4cCI6MTczODk0Njg1OCwiaWF0IjoxNzM4OTAzNjU5LCJuYmYiOjE3Mzg5MDM2NTksImNsaWVudF9pZCI6InJhZ2dlbmllLWJhY2tlbmQiLCJqdGkiOiJWMl8zMDYwMjkyNjkyOTE2MzA1OTUtYXRfMzA2MDI5MjY5MjkxNjk2MTMxIn0.vK65bFc3eoPc0qp3zz9vj1Hi1LOctqWpMOanYXw4GQCoXjdfWCZSLZXjkfyARydyN0-zPnjV_KEb35Rh9UmmUpu0D1fRWHN8Owm1FtZ5ccJ9c_gD7VvMaH7c1PNi3dWQOQPyunl9jivpFvsXsWXhuA8Dyjeq9wnam982qQW7dSfdabuVTrMQK-YRDmHmLESroS71Zf4CdZv9P9wc9Phm082Hs-rwQanPcEV08vzgx40Q_DwlULBbiJ33qAhA76GktvKqhJM48t69ZzsnPOvzn8COzyu4MBqai2-8G0BVvbzP5kmRqmjl_RuwGmJkiSlyi0AaeXduB2wE0bT1S1BN9Q")
    zitadel_domain: str = os.getenv("ZITADEL_DOMAIN", "http://localhost:8080")
    retry_limit:int = os.getenv("RETRY_LIMIT",0)
    application_port: int = os.getenv("APP_PORT", 8001)
    


configs = Configs()
