from sqlalchemy.orm import Session
import app.models.user as models
import app.schemas.user as schemas
from sqlalchemy.exc import SQLAlchemyError

def create_user(user: schemas.UserCreate, db: Session):
    try:
        db_user = models.User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user, False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def get_user_by_id(user_id: int, db: Session):
    try:
        return db.query(models.User).filter(models.User.id == user_id).first(), False
    except SQLAlchemyError as e:
        return str(e), True
