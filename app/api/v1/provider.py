from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.schemas.common as resp_schemas
import app.schemas.provider as schemas
from app.utils.database import get_db
import app.services.provider as svc
import app.api.v1.commons as commons
from fastapi import Request

router = APIRouter()
sample = APIRouter()


@router.get("/list", response_model=resp_schemas.CommonResponse)
def list_providers(db: Session = Depends(get_db)):

    """
    Retrieves a list of providers (plugins) from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing either the list of providers or an error message.
    """

    result, error = svc.list_providers(db)

    if error:
        return commons.is_error_response("DB error", result, {"providers": []})

    if not result:
        return commons.is_none_reponse("Providers Not Found", {"providers": []})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"providers": result},
        message="Providers Found",
        error=None
    )

@router.get("/get/{provider_id}", response_model=resp_schemas.CommonResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):

    """
    Retrieves a specific provider (plugin) by its ID.

    Args:
        provider_id (int): The ID of the provider to retrieve.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing either the provider details or an error message.
    """

    result, error=svc.get_provider(provider_id, db)

    if error:
        return commons.is_error_response("DB error", result, {"provider": {}})

    if not result:
        return commons.is_none_reponse("Providers Not Found", {"provider": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"provider": result},
        message="Provider not Found",
        error=None
    )

@router.post("/{provider_id}/test-credentials", response_model=resp_schemas.CommonResponse)
def test_connections(provider_id: int, config: schemas.TestCredentials, db: Session = Depends(get_db)):

    """
    Tests the credentials for a specific provider (plugin) by its ID.

    Args:
        provider_id (int): The ID of the provider for which to test credentials.
        config (TestCredentials): The credentials to test.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the credential test.
    """

    success, message = svc.test_credentials(provider_id, config, db)

    if not success:
        return resp_schemas.CommonResponse(
            status=False,
            status_code=422,
            message=message,
            error=message,
        )

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message=message,
        error=None,
    )

@router.get("/llmproviders", response_model=resp_schemas.CommonResponse)
def getllmproviders(request: Request):

    """
    Retrieves a list of available LLM (Large Language Model) providers.

    Args:
        request (Request): The HTTP request object.

    Returns:
        CommonResponse: A response containing either the list of LLM providers or an error message.
    """

    result, is_error = svc.getllmproviders(request)

    if is_error:
        return resp_schemas.CommonResponse(
            status=False,
            status_code=422,
            message="LLM providers not found",
            error=None,
        )

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="LLM providers found",
        data=result,
        error=None,
    )

@sample.get("/list", response_model=resp_schemas.CommonResponse)
def list_sql(db: Session = Depends(get_db)):

    """
    Retrieves a list of sample SQL records from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing either the list of sample SQL records or an error message.
    """

    result, error = svc.listsql(db)

    if error:
        return commons.is_error_response("DB error", result, {"sql": []})

    if not result:
        return commons.is_none_reponse("Sample SQL Not Found", {"sql": []})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"sql": result},
        message="Sample SQL Found",
        error=None
    )

@sample.get("/{id}", response_model=resp_schemas.CommonResponse)
def get_sql(id: int, db: Session = Depends(get_db)):

    """
    Retrieves a specific sample SQL record by its ID.

    Args:
        id (int): The ID of the sample SQL record to retrieve.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing either the SQL record or an error message.
    """

    result, error = svc.getsql(id, db)

    if error:
        return commons.is_error_response("DB error", result, {"sql": {}})

    if not result:
        return commons.is_none_reponse("Sample SQL Not Found", {"sql": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"sql": result},
        message="Sample SQL Found",
        error=None
    )



@sample.post("/create", response_model=resp_schemas.CommonResponse)
def create_sql(request:Request,sql: schemas.SampleSQLBase, db: Session = Depends(get_db)):

    """
    Creates a new sample SQL record in the database.

    Args:
        request (Request): The HTTP request object.
        sql (SampleSQLBase): The data for the new SQL record.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the SQL creation process.
    """

    result, error = svc.create_sql(request, sql, db)

    if error:
        return commons.is_error_response("DB error", result, {"sql": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        message="Sample SQL Created Successfully",
        error=None,
        data={"SQL": result}
    )

@sample.post("/update/{id}", response_model=resp_schemas.CommonResponse)
def update_sql(id: int, request: Request, sql: schemas.SampleSQLUpdate, db: Session = Depends(get_db)):

    """
    Updates an existing sample SQL record by its ID.

    Args:
        id (int): The ID of the SQL record to update.
        request (Request): The HTTP request object.
        sql (SampleSQLUpdate): The updated SQL data.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the SQL update process.
    """

    result, error = svc.update_sql(request, id, sql, db)

    if error:
        return commons.is_error_response("DB error", result, {"sql": {}})

    if not result:
        return commons.is_none_reponse("Sample SQL Not Found", {"sql": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Sample SQL Updated Successfully",
        error=None,
        data={"sql": result}
    )

@sample.delete("delete/{id}", response_model=resp_schemas.CommonResponse)
def delete_sql(id: int, db: Session = Depends(get_db)):

    """
    Deletes a sample SQL record by its ID.

    Args:
        id (int): The ID of the SQL record to delete.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the SQL deletion process.
    """

    result, error = svc.delete_sql(id, db)

    if error:
        return commons.is_error_response("DB error", result, {"sql": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Sample SQL Deleted Successfully",
        error=None,
    )