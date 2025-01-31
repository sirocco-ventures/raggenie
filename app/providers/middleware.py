from app.providers.config import configs
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi import HTTPException, Security
import httpx

http_bearer = HTTPBearer()

 
async def introspect_token(token: str):
    url = configs.cintrospection_url
    client_id = configs.cclient_id
    client_secret = configs.cclient_secret

    async with httpx.AsyncClient() as client:
       
        response = await client.post(
            url,
            data={"token": token},
            headers={
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'   
            },
            auth=(client_id, client_secret),
        )

        

        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail='Token Introspection Failed')

        
        data = response.json()

         
        if not data.get('active'):
            raise HTTPException(status_code=401, detail="Inactive Token")

        
        return data


 
async def verify_token(auth: str = Security(http_bearer)):
    token = auth.credentials
     
    user_data = await introspect_token(token)
    
    return user_data
