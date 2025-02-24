from sqlalchemy.orm import Session
import app.models.environment as models
import app.schemas.environment as schemas
from sqlalchemy.exc import SQLAlchemyError

def create_environment(name: str, db: Session):
    """ creates a new environment with a given name"""
    new_env = models.Environment(name=name)
    db.add(new_env)
    db.commit()
    db.refresh(new_env)
    return new_env

def get_or_create_default_environment(db: Session):
    default_env = db.query(models.Environment).filter(models.Environment.name == "Default Environment").first()

    if not default_env:
        default_env = models.Environment(name="Default Environment", is_active=True)
        db.add(default_env)
        db.commit()
        db.refresh(default_env)

    return default_env

def assign_user_to_environment(user_id: int, environment_id: int, db: Session):
    try:
        user_env_mapping = models.UserEnvironmentMapping(user_id=user_id, environment_id=environment_id,  is_active=True)
        db.add(user_env_mapping)
        db.commit()
        return user_env_mapping, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)
