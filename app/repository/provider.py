from sqlalchemy.orm import Session
import app.models.provider as models
import app.models.connector as conn_model
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Dict
import app.schemas.provider as schemas

from app.models.environment import UserEnvironmentMapping


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

def list_sql(db:Session, user_id: str):
    try:
        active_env = (db.query(UserEnvironmentMapping)
            .filter(UserEnvironmentMapping.user_id == user_id, UserEnvironmentMapping.is_active == True)
            .first())
        sql = (
            db.query(models.SampleSQL)
            .filter(models.SampleSQL.environment_id == active_env.id)
            .all()
        )
        return sql, False
    except SQLAlchemyError as e:
        return e, True

def get_sql(id:int,db:Session):
    try:
        return db.query(models.SampleSQL).filter(models.SampleSQL.id == id).first(), False
    except SQLAlchemyError as e:
        return e, True

def create_sql(sql:schemas.SampleSQLBase, db:Session, user_id: str):

    try:
        active_env = (db.query(UserEnvironmentMapping)
            .filter(UserEnvironmentMapping.user_id == user_id, UserEnvironmentMapping.is_active == True)
            .first())
        db_sql = models.SampleSQL(
            description=sql.description,
            sql_metadata=sql.sql_metadata,
            connector_id = sql.connector_id,
            environment_id = active_env.id
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

def revoke_existing_vectordb_confg(id: int, db: Session):
    """
    Revoke (delete) existing VectorDB configurations based on vector_db_id.

    Args:
        id (int): The vector_db_id to delete the mappings for.
        db (Session): Database session object.

    Returns:
        Tuple: (Success message or error, Boolean indicating if an error occurred)
    """
    try:
        existing_mappings = db.query(models.VectorDB).join(models.VectorDBConfigMapping)\
            .filter(models.VectorDBConfigMapping.vector_db_id == id).all()

        for mapping in existing_mappings:
            db.delete(mapping)

        db.commit()

        return "VectorDB configurations revoked successfully", False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True



def create_vectordb_with_embedding(key,id, vectordb, db: Session):

    if key == "update":
        result, is_error = revoke_existing_vectordb_confg(id, db)

        if is_error:
            return result, True

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

        if vectordb.embedding_config:
            db_embedding = models.Embeddings(
                provider=vectordb.embedding_config['provider'],
                config=vectordb.embedding_config['params'],
            )
            db.add(db_embedding)
            db.commit()
            db.refresh(db_embedding)

            db_embedding_mapping = models.VectorEmbeddingMapping(
                vector_db_id=db_vectordb.id,
                embedding_id=db_embedding.id,
            )
            db.add(db_embedding_mapping)
            db.commit()
            db.refresh(db_embedding_mapping)

            return {
                'vectordb': db_vectordb,
                'vectordb_mapping': db_vectordb_mapping,
                'embedding': db_embedding,
            }, False

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
        db_vectordb = db.query(models.VectorDB).join(models.VectorDBConfigMapping)\
            .options(joinedload(models.VectorDB.vectordb_config_mapping))\
            .filter(models.VectorDBConfigMapping.config_id == id).first()

        embedding = db.query(models.Embeddings).join(models.VectorEmbeddingMapping)\
                    .filter(models.VectorEmbeddingMapping.vector_db_id == db_vectordb.id).first()

        if not db_vectordb:
            return "VectorDB not found", True

        if not embedding:
            return "No embedding found for VectorDB", True

        return (db_vectordb, embedding), False

    except SQLAlchemyError as e:
        return str(e), True

def get_mapped_vector_store(db: Session, config_id: int):
    try:

        vectordb = db.query(models.VectorDB).join(models.VectorDBConfigMapping, models.VectorDB.id == models.VectorDBConfigMapping.vector_db_id)\
            .options(joinedload(models.VectorDB.vectordb_config_mapping))\
            .filter(models.VectorDBConfigMapping.config_id == config_id).first()

        if not vectordb:
            return None, False

        embedding = db.query(models.Embeddings).join(models.VectorEmbeddingMapping, models.Embeddings.id == models.VectorEmbeddingMapping.embedding_id)\
            .filter(models.VectorEmbeddingMapping.vector_db_id == vectordb.id).first()

        embedding_details = {
            "vectordb": vectordb.vectordb,
            "vectordb_config": vectordb.vectordb_config,
        }

        if embedding:
            embedding_details.update({
                "em_provider": embedding.provider,
                "embedding_config": embedding.config
            })

        return embedding_details, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True