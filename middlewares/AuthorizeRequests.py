from fastapi import  Request
from utils.ResponseTypes import ErrorResponse
from db.mongodb.init import MongoDB
from fastapi import status


async def AuthorizeAccess(request:Request,call_next):
    
    fromSameOrigin:bool =  request.headers.get('sec-fetch-site') == 'same-origin'
    if fromSameOrigin :  
        return await call_next(request)
    
    collection =  MongoDB.getInstance()['audioServerDev']['ApiKeys']
    api_key = request.headers.get('x-api-key')
    
    if api_key is None: 
        return ErrorResponse(message="",code=status.HTTP_400_BAD_REQUEST)
    
    doc = await collection.find_one({'key':api_key})
    
    if doc is None : 
        return ErrorResponse(message="Forbidden",code=status.HTTP_403_FORBIDDEN)
    
    permissions = list(doc['permissions'])
    
    if not ("GENERAL" in permissions) : 
        return ErrorResponse(message="You don't have permission",code=status.HTTP_401_UNAUTHORIZED)
    
    return await call_next(request)
    
    

