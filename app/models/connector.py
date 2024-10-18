from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Connector(Base):
    __tablename__ = 'connectors'

    id = Column(Integer, primary_key=True, index=True)
    connector_type = Column(Integer, ForeignKey('providers.id'), nullable=False)
    connector_name = Column(String, nullable=False, index=True)
    connector_description = Column(String, nullable=True, index=True)
    connector_config = Column(JSON, nullable=False)
    schema_config = Column(JSON, nullable=True)
    connector_docs = Column(Text, nullable=True)
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    provider = relationship('Provider', back_populates='connectors')
    actions = relationship('Actions', back_populates='connectors', cascade="all,delete")
    sample_sql = relationship('SampleSQL', back_populates='connectors')



class Configuration(Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True, index=True)
    name= Column(String, nullable=False)
    short_description = Column(String, nullable=False, index=True)
    long_description = Column(String, nullable=True, index=True)
    enable = Column(Boolean, default=True)
    status = Column(Integer, default=0, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    capabilities = relationship('Capabilities', back_populates='configuration', cascade="all,delete")
    inference_mapping = relationship('Inferenceconfigmapping', back_populates='configuration')



class Capabilities(Base):
    __tablename__ = 'capabilities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description=Column(String, nullable=False)
    requirements=Column(JSON, nullable=False)
    config_id = Column(Integer, ForeignKey('configurations.id'))
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    configuration = relationship('Configuration', back_populates='capabilities')
    cap_actions_mapping = relationship('CapActionsMapping', back_populates='capabilities')

class Inference(Base):
    __tablename__ = 'inference'

    id =  Column(Integer, primary_key=True, index=True)
    name = Column(String,  nullable=False)
    llm_provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    endpoint= Column(String, nullable=False)
    apikey=Column(String, nullable=False)
    enable= Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    inference_mapping = relationship('Inferenceconfigmapping', back_populates='inference')


class Inferenceconfigmapping(Base):
    __tablename__ ='inferenceconfigmapping'

    id = Column(Integer, primary_key=True, index=True)
    inference_id = Column(Integer, ForeignKey('inference.id'))
    config_id = Column(Integer, ForeignKey('configurations.id'))
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    inference = relationship('Inference', back_populates='inference_mapping')
    configuration = relationship('Configuration', back_populates='inference_mapping')


class Actions(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    types = Column(String, nullable=False)
    body = Column(JSON, nullable=False)
    table = Column(String, nullable=True)
    enable = Column(Boolean, default=True)
    condition = Column(JSON, default=None)
    connector_id = Column(Integer, ForeignKey("connectors.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    connectors = relationship('Connector', back_populates='actions')
    cap_actions_mapping = relationship('CapActionsMapping', back_populates='actions')

class CapActionsMapping(Base):
    __tablename__ = 'cap_actions_mapping'

    id = Column(Integer, primary_key=True, index=True)
    capability_id = Column(Integer, ForeignKey('capabilities.id'))
    action_id = Column(Integer, ForeignKey('actions.id'))
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    capabilities = relationship('Capabilities', back_populates='cap_actions_mapping')
    actions = relationship('Actions', back_populates= 'cap_actions_mapping')