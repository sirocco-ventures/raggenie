from app.models.db import Base
from app.utils.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


class ContextStorage:
    def __init__(self,db: Session=Depends(get_db)):
        self.session = db
        self.engine = self.session.get_bind()


    def create_table(self):
        Base.metadata.create_all(self.engine)

    def insert_data(self, data):
        self.session.add(data)
        self.session.commit()

    def update_data(self, model, filters, updates):
        self.session.query(model).filter_by(**filters).update(updates)
        self.session.commit()

    def query_data(self, model,  filters=None, limit=None):
        query = self.session.query(model)
        if filters:
            query = query.filter_by(**filters)


        if limit:
            query = query.limit(limit)

        results = query.all()
        return results