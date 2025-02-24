from sqlalchemy.orm import Session
import app.repository.user as repo
import app.repository.environment as env_repo
import app.schemas.user as schemas

def get_or_create_user(user: schemas.UserCreate, db: Session):
    """
    Retrieves an existing user or creates a new one if not found.
    
    Args:
        user (UserBase): The data for the new user.
        db (Session): Database session dependency.

    Returns:
        Tuple: UserResponse object and error message (if any).
    """
    
    existing_user, is_error = repo.get_user_by_id(user.id, db)
    if existing_user:
        return existing_user, None
    
    new_user, is_error = repo.create_user(user, db)
    if is_error:
        return None, "Failed to create user"
    
    unique_env = env_repo.create_environment(f"{new_user.username} env", db)
    assign_result, env_error = env_repo.assign_user_to_environment(new_user.id, unique_env.id, db)
    
    if env_error:
        return None, f"User created but failed to assign environment: {env_error}"

    user_response = schemas.UserResponse(
        id=new_user.id,
        username=new_user.username,
    )

    return user_response, None