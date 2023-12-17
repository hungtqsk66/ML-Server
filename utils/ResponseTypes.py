from fastapi import status
from starlette.responses import JSONResponse

def SuccessResponse(data,code = status.HTTP_200_OK,message="Success")->JSONResponse:
    
    return JSONResponse( 
            status_code=code,
            content={
                "statusCode":code,
                "message":message,
                "metadata":data
    })
    
def ErrorResponse(message="Something went wrong",code = status.HTTP_500_INTERNAL_SERVER_ERROR)->JSONResponse:

    return JSONResponse(
            status_code=code,
            content={
                "statusCode":code,
                "message":message,
    })