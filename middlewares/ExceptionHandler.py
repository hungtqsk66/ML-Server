from fastapi import  Request
from utils.ResponseTypes import ErrorResponse
import traceback

async def HandleExceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except:
        traceback.print_exc()
        return ErrorResponse()