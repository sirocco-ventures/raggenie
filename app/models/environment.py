from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.utils.database import Base
from sqlalchemy.orm import relationship


class Environment(Base):
    __tablename__ = "environments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    configurations = relationship("Configuration", back_populates="environment") 
    connectors = relationship("Connector", back_populates="environment") 
    sample_sql = relationship("SampleSQL", back_populates="environment") 

class UserEnvironmentMapping(Base):
    __tablename__ = "user_environment_mapping"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    environment_id = Column(Integer, ForeignKey('environments.id'), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
