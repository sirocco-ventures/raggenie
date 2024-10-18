from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    providers = relationship('Provider', back_populates='category')

class Provider(Base):
    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    key = Column(String, unique=True, nullable=False, index=True)
    icon = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    connectors = relationship('Connector', back_populates='provider')
    category = relationship('Category', back_populates='providers')
    providerconfig = relationship('ProviderConfig', back_populates='provider')

class ProviderConfig(Base):
    __tablename__ = "providerconfig"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    field = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    value = Column(JSON, nullable=True)
    enable = Column(Boolean, default=True)
    config_type= Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    required=Column(Boolean, nullable=True, default=True)
    provider_id = Column(Integer, ForeignKey('providers.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    provider = relationship('Provider', back_populates='providerconfig')

class VectorDBConfig(Base):
    __tablename__ = "vectordbconfig"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    key = Column(String, unique=True, nullable=False, index=True)
    icon = Column(String, nullable=False)
    config = Column(JSON)
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

class SampleSQL(Base):
    __tablename__ = "sample_sql"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    sql_metadata = Column(JSON, nullable=True)
    connector_id = Column(Integer, ForeignKey('connectors.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    connectors = relationship('Connector', back_populates='sample_sql')

class VectorDB(Base):
    __tablename__ = "vectordb"

    id = Column(Integer, primary_key=True, index=True)
    vectordb = Column(String, nullable=False)
    vectordb_config = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vectordb_config_mapping = relationship('VectorDBConfigMapping', back_populates='vector_db')
    vector_embedding_mapping = relationship('VectorEmbeddingMapping', back_populates='vector_db')



class VectorDBConfigMapping(Base):
    __tablename__ = "vectordb_config_mapping"

    id = Column(Integer, primary_key=True, index=True)
    vector_db_id = Column(Integer, ForeignKey('vectordb.id'), nullable=False)
    config_id = Column(Integer, ForeignKey('configurations.id'), nullable=False)
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vector_db = relationship('VectorDB', back_populates='vectordb_config_mapping')
    configuration = relationship('Configuration', back_populates='vectordb_config_mapping')

class Embeddings(Base):
    __tablename__ = "embeddings_configs"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)
    config = Column(JSON, nullable=False)
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vector_embedding_mapping = relationship("VectorEmbeddingMapping", back_populates= "embeddings_config")

class VectorEmbeddingMapping(Base):
    __tablename__ = "vector_embedding_mapping"

    id = Column(Integer, primary_key=True, index=True)
    vector_db_id = Column(Integer, ForeignKey('vectordb.id'), nullable=False)
    embedding_id = Column(Integer, ForeignKey('embeddings_configs.id'), nullable=False)
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vector_db = relationship('VectorDB', back_populates='vector_embedding_mapping')
    embeddings_config = relationship('Embeddings', back_populates='vector_embedding_mapping')