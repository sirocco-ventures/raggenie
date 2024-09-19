
import app.schemas.common as resp_schemas

def is_error_response(message:str, err:str, data:dict):
    return resp_schemas.CommonResponse(
            status= False,
            status_code=422,
            message=message,
            data=data,
            error=err
        )

def is_none_reponse(message:str, data:dict):
    return resp_schemas.CommonResponse(
            status= True,
            status_code=200,
            message=message,
            data=data,
            error="Not Found"
        )