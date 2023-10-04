from fastapi import  Request
from utils.Response.response_types import ErrorResponse
from db.mongodb.init import MongoDB
from fastapi import status


async def check_API_Key(request:Request,call_next):
    
    collection =  MongoDB.getInstance()['audioServerDev']['ApiKeys']
    
    api_key = request.headers.get('x-api-key')
    
    if not api_key: return ErrorResponse(message="Missing header value",code=status.HTTP_400_BAD_REQUEST)
    
    doc = collection.find_one({'key':api_key})
    
    if not doc : return ErrorResponse(message="Not valid header",code=status.HTTP_400_BAD_REQUEST)
    
    permissions = list(doc['permissions'])
    
    if not ("GENERAL" in permissions) : return ErrorResponse(message="You don't have permission",code=status.HTTP_401_UNAUTHORIZED)
    
    return await call_next(request)
    
    

