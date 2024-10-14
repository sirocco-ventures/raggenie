from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime


class ProviderConfigBase(BaseModel):
    name: str
    description: str
    field: str
    slug: str
    provider_id: int
    config_type:int
    order:int
    required:bool
    value:Any

class ProviderConfigResponse(ProviderConfigBase):
    id: int

class ProviderBase(BaseModel):
    name: str
    description: str
    icon: str
    category_id: int
    enable: Optional[bool] = True

class ProviderResp(ProviderBase):
    id:int
    key: str
    configs: List[ProviderConfigResponse]

class ProviderCreate(ProviderBase):
    pass

class ProviderUpdate(ProviderBase):
    pass

class ProviderInDBBase(ProviderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Provider(ProviderInDBBase):
    pass

class ProviderList(BaseModel):
    providers: List[Provider]


class CategoryBase(BaseModel):
    name: str
    description: str
    enable: Optional[bool] = True

class CategoryResponse(CategoryBase):
    id: int


class CategoryCreate(CategoryBase):
    pass

class CategoryList(BaseModel):
    categories: List[CategoryResponse]


class ProviderConfigBase(BaseModel):
    name: str
    description: str
    field: str
    slug: str
    enable: Optional[bool] = True
    provider_id: int

class ProviderConfigResponse(ProviderConfigBase):
    id: int

class ProviderConfigList(BaseModel):
    category: List[ProviderConfigResponse]



class TestCredentials(BaseModel):
    provider_config: Dict[str, Any]

class TestVectorDBCredentials(BaseModel):
    vectordb_config: Dict[str, Any]

class SampleSQLBase(BaseModel):
    description: str
    sql_metadata: Optional[Dict] = None
    connector_id: int

class SampleSQLUpdate(BaseModel):
    description: Optional[str] = None
    sql_metadata: Optional[Dict] = None
    connector_id: Optional[int] = None

class SampleSQLResponse(SampleSQLBase):
    id: int

class VectorDBConfigBase(BaseModel):
    name: str
    description: str
    key: str
    icon: str
    config: List[Dict[str,Any]]

class VectorDBConfigResponse(VectorDBConfigBase):
    id: int

class VectorDBUpdateBase(BaseModel):
    vectordb: Optional[str] = None
    vector_config : Optional[List[Dict[str,Any]]] = None
    config_id: Optional[int] = None

class VectorDBBase(BaseModel):
    vectordb: str
    vector_config : List[Dict[str,Any]]
    config_id: int

class VectorDBResponse(VectorDBBase):
    id: int
