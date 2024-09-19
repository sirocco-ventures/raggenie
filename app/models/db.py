from sqlalchemy import  Column, Integer, String, DATETIME
from sqlalchemy.orm import  declarative_base

Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    context_id = Column(String, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    created_at = Column(DATETIME, nullable=False)