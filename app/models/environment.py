from sqlalchemy import Column, Integer, String, ForeignKey
from app.utils.database import Base

class Environment(Base):
    __tablename__ = "environments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class UserEnvironmentMapping(Base):
    __tablename__ = "user_environment_mapping"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    environment_id = Column(Integer, ForeignKey('environments.id'), nullable=False)
