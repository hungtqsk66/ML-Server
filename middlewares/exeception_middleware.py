from fastapi import  Request
from utils.Response.response_types import ErrorResponse

async def handle_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(e)
        return ErrorResponse()