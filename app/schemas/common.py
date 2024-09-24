from pydantic import BaseModel
from typing import Optional, Any

class DBConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    dbname: str

class CommonResponse(BaseModel):
    status: bool
    status_code: int
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None