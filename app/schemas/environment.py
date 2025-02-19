from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EnvironmentBase(BaseModel):
    name: str

class EnvironmentResponse(EnvironmentBase):
    id: int

class UserEnvironmentMappingBase(BaseModel):
    user_id: int
    environment_id: int

class UserEnvironmentMappingResponse(UserEnvironmentMappingBase):
    id: int