from sqlalchemy.orm import Session
import app.models.provider as models
import app.models.connector as conn_model
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Dict
import app.schemas.provider as schemas


def insert_or_update_data(db: Session, model: Any, filters: Dict[str, Any], data: Dict[str, Any]) -> tuple:
    try:
        existing_record = db.query(model).filter_by(**filters).first()

        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)

            db.commit()
            db.refresh(existing_record)
            return existing_record, False
        else:
            new_record = model(**data)
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            return new_record, False

    except SQLAlchemyError as e:
        db.rollback()
        db.expunge_all()
        return str(e), True



def get_all_providers(db: Session):
    try:
        return db.query(models.Provider).options(joinedload(models.Provider.providerconfig)).all(), False
    except SQLAlchemyError as e:
        return e, True

def get_provider_by_id(provider_id: int, db: Session):
    try:
        provider = db.query(models.Provider).options(joinedload(models.Provider.providerconfig)).filter(models.Provider.id == provider_id).first()
        return provider, False
    except SQLAlchemyError as e:
        return e, True
def get_vector_db_config(db: Session, key: str):
    try:
        return db.query(models.VectorDBConfig).filter(models.VectorDBConfig.key==key).first(), False
    except SQLAlchemyError as e:
        return e, True

def get_vectordb_providers(db:Session):
    try:
        return db.query(models.VectorDBConfig).all(), False
    except SQLAlchemyError as e:
        return e, True

def get_config_types(provider_id: int, db:Session):
    try:
        return db.query(models.ProviderConfig).filter(models.ProviderConfig.provider_id==provider_id).all(), False
    except SQLAlchemyError as e:
        return e, True

def get_sql_by_connector(id:int, db:Session):
    try:
        return db.query(models.SampleSQL).filter(models.SampleSQL.connector_id == id).all(), False
    except SQLAlchemyError as e:
        return e, True

def list_sql(db:Session):
    try:
        return db.query(models.SampleSQL).all(), False
    except SQLAlchemyError as e:
        return e, True

def get_sql(id:int,db:Session):
    try:
        return db.query(models.SampleSQL).filter(models.SampleSQL.id == id).first(), False
    except SQLAlchemyError as e:
        return e, True

def create_sql(sql:schemas.SampleSQLBase, db:Session):

    try:
        db_sql = models.SampleSQL(
            description=sql.description,
            sql_metadata=sql.sql_metadata,
            connector_id = sql.connector_id,
        )
        db.add(db_sql)
        db.commit()
        db.refresh(db_sql)
        return db_sql, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def update_sql(sql_id:int, sql:schemas.SampleSQLUpdate, db:Session):
    try:
        db_sql = db.query(models.SampleSQL).filter(models.SampleSQL.id == sql_id).first()

        if db_sql is None:
            return "Data is None", True

        db_sql.description = sql.description if sql.description else db_sql.description
        db_sql.sql_metadata = sql.sql_metadata if sql.sql_metadata else db_sql.sql_metadata
        db_sql.connector_id = sql.connector_id if sql.connector_id else db_sql.connector_id
        db.commit()
        return db_sql, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True


def delete_sql(sql_id:int, db: Session):
    try:
        db_sql = db.query(models.SampleSQL).filter(models.SampleSQL.id == sql_id).first()
        if db_sql is None:
            return "Data is None", True
        db.delete(db_sql)
        db.commit()
        return None, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def get_sql_by_key(key: str, db: Session):
    try:
        return db.query(models.SampleSQL).options(joinedload(models.SampleSQL.connectors)).filter(conn_model.Connector.connector_name == key).first(), False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e),True

def create_vectordb_instance(vectordb, db: Session):
    try:
        db_vectordb = models.VectorDB(
            vectordb=vectordb.vectordb,
            vectordb_config=vectordb.vectordb_config,
        )
        db.add(db_vectordb)
        db.commit()
        db.refresh(db_vectordb)

        db_vectordb_mapping = models.VectorDBConfigMapping(
            vector_db_id=db_vectordb.id,
            config_id=vectordb.config_id,
        )
        db.add(db_vectordb_mapping)
        db.commit()
        db.refresh(db_vectordb_mapping)

        return (db_vectordb, db_vectordb_mapping), False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def create_embedding_instance(vector_db_id,vectordb, db: Session):
    try:
        db_embedding = models.Embeddings(
            provider=vectordb.embedding_config.provider,
            config = vectordb.embedding_config.params
        )
        db.add(db_embedding)
        db.commit()
        db.refresh(db_embedding)

        db_embedding_mapping = models.VectorEmbeddingMapping(
            vector_db_id=vector_db_id,
            config_id=vectordb.config_id,
        )
        db.add(db_embedding_mapping)
        db.commit()
        db.refresh(db_embedding_mapping)

        return (db_embedding, db_embedding_mapping), False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True


def get_vectordb_instance(id: int, db: Session):
    """
    Retrieves a VectorDB instance by its ID, along with its associated VectorDBConfigMapping, using joinedload.

    Args:
        id (int): The ID of the VectorDB instance.
        db (Session): Database session object.

    Returns:
        Tuple: The VectorDB instance and its associated config mapping, or an error message.
    """

    try:
        db_vectordb = db.query(models.VectorDB).options(
            joinedload(models.VectorDB.vectordb_config_mapping)
        ).filter(models.VectorDB.id == id).first()

        if not db_vectordb:
            return "VectorDB not found", True


        return db_vectordb, False

    except SQLAlchemyError as e:
        return str(e), True

def delete_vectordb_instance(id: int, db: Session):
    """
    Deletes a VectorDB instance and its associated config mapping by ID.

    Args:
        id (int): The ID of the VectorDB instance to delete.
        db (Session): Database session object.

    Returns:
        Tuple: Success message and error flag.
    """
    try:
        db_vectordb = db.query(models.VectorDB).filter(models.VectorDB.id == id).first()

        if not db_vectordb:
            return "VectorDB instance not found", True

        db.query(models.VectorDBConfigMapping).filter(
            models.VectorDBConfigMapping.vector_db_id == id
        ).delete()

        db.delete(db_vectordb)
        db.commit()

        return "VectorDB instance deleted successfully", False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def update_vectordb_instance(id: int, vectordb: schemas.VectorDBBase, db: Session):
    """
    Updates a VectorDB instance and its associated config mapping by ID.

    Args:
        id (int): The ID of the VectorDB instance to update.
        vectordb (schemas.VectorDBBase): The updated data for the VectorDB instance.
        db (Session): Database session object.

    Returns:
        Tuple: Updated VectorDB instance and error flag.
    """
    try:
        db_vectordb = db.query(models.VectorDB).options(
            joinedload(models.VectorDB.vectordb_config_mapping)
        ).filter(models.VectorDB.id == id).first()

        if not db_vectordb:
            return "VectorDB instance not found", True

        db_vectordb.vectordb = vectordb.vectordb if vectordb.vectordb else db_vectordb.vectordb
        db_vectordb.vectordb_config = vectordb.vectordb_config if vectordb.vectordb_config else db_vectordb.vectordb_config

        for mapping in db_vectordb.vectordb_config_mapping:
            mapping.config_id = vectordb.config_id if vectordb.config_id else mapping.config_id

        db.commit()
        db.refresh(db_vectordb)

        return db_vectordb, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def get_mapped_vector_store(db:Session, config_id:int):
    try:
        return db.query(models.VectorDB).join(models.VectorDBConfigMapping, models.VectorDB.id == models.VectorDBConfigMapping.vector_db_id)\
            .options(joinedload(models.VectorDB.vectordb_config_mapping))\
            .filter(models.VectorDBConfigMapping.config_id == config_id).first()  , False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True