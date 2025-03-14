from pydantic import BaseModel
from typing import List, Dict, Optional, Union
from app.schemas.provider import VectorDBResponse
class ConnectorBase(BaseModel):
    connector_type: int
    connector_name: str
    connector_description: Optional[str] = None
    connector_config: dict
    schema_config: Optional[Union[List[Dict], Dict]] = None
    connector_docs: Optional[str]= None
    enable: Optional[bool] = True

class ConnectorResponse(ConnectorBase):
    connector_id:int
    connector_key :Optional[str]=None
    icon:Optional[str]=None
    provider_id: Optional[int] = None

class ConnectorUpdate(BaseModel):
    connector_type: Optional[int] = None
    connector_name: Optional[str] = None
    connector_description: Optional[str] = None
    connector_config: Optional[dict] = None
    connector_docs: Optional[str]= None
    schema_config: Optional[List[Dict]] = None

class SchemaUpdate(BaseModel):
    schema_config : Optional[List[Dict]]=None

class CapabilitiesBase(BaseModel):
    id:Optional[int]=None
    name:str
    description:str
    requirements:List[Dict]
    config_id:Optional[int]=None
    actions_list: Optional[List[int]]=None
    actions:Optional[List[Dict]]=None

class CapabilitiesArray(BaseModel):
    capabilities:List[CapabilitiesBase]

class CapabilitiesUpdateBase(BaseModel):
    id:Optional[int]=None
    name:Optional[str]=None
    description:Optional[str]=None
    requirements:Optional[List[Dict]]=None
    config_id:Optional[int]=None
    actions_list: Optional[List[int]]=None

class ConfigurationBase(BaseModel):
    short_description: str
    long_description: Optional[str]
    name:str
    status: int

class ConfigurationCreation(ConfigurationBase):
    capabilities: List[int]
    connectors: List[int]



class ConfigurationUpdate(BaseModel):
    name:Optional[str]=None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    status: Optional[int] = 0
    capabilities: Optional[List[int]]=None
    connectors: List[int]


class InferenceBase(BaseModel):
    name:str
    apikey:str
    llm_provider:str
    model:str
    config_id:Optional[int]=None
    endpoint:str

class InferenceBaseUpdate(BaseModel):
    name:Optional[str]=None
    apikey:Optional[str]=None
    llm_provider:Optional[str]=None
    model:Optional[str]=None
    config_id:Optional[int]=None
    endpoint:Optional[str]=None

class InferenceResponse(InferenceBase):
    id:int

class ConfigurationResponse(ConfigurationBase):
    id: int
    capabilities: List[CapabilitiesBase]
    inference: Optional[List[InferenceResponse]]=None
    vectordb: Optional[List[VectorDBResponse]]=None
    connector: Optional[List[ConnectorResponse]]=None

class Actions(BaseModel):
    name: str
    description: Optional[str] = None
    types: str
    condition: Optional[Dict] = None
    table : Optional[str] = None
    connector_id: Optional[int] = None
    body : Dict


class ActionsResponse(Actions):
    id: int
    enable: Optional[bool] =True

class ActionsUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    types: Optional[str] = None
    condition: Optional[Dict] = None
    table : Optional[str] = None
    connector_id: Optional[int] = None
    body : Optional[Dict] = None

class LLMProviderBase(BaseModel):
    key:str
    api_key:str
    kind:Optional[str]=None
    unique_name: Optional[str]=None