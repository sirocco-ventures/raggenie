from app.providers.config import configs
from fastapi import HTTPException
from fastapi import HTTPException
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi import HTTPException, Security
from app.providers.config import configs
import httpx
http_bearer = HTTPBearer()



async def introspect_token(token:str):
    url = configs.cintrospection_url
    client_id = configs.cclient_id
    client_secret = configs.cclient_secret

    async with httpx.AsyncClient() as client :
        resposne = await client.post(
            url,
            data={"token":token},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=(client_id, client_secret),
        )
        
        if resposne.status_code !=200 :
            raise HTTPException(status_code=resposne.status_code,detail='Token Introspection Fail')
        data = resposne.json()
        if not data.get('active'):
            raise HTTPException(status_code=401,detail="Inactive Token")
        return resposne.json()



async def verify_token(auth:str =Security(http_bearer)):
    token = auth.credentials
    user_data = await introspect_token(token)
    return user_data
    


    
