from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from middlewares.ExceptionHandler import HandleExceptions
from middlewares.AuthorizeRequests import AuthorizeAccess
from Controllers.Model_Controller import model_controller


router = APIRouter(prefix='/api/ml-server')

router.include_router(model_controller)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.middleware('http')
async def AuthorizeRequestAccess_Middleware(request: Request, call_next):
    return await AuthorizeAccess(request,call_next)

@app.middleware('http')
async def ExceptionHandling_middleware(request: Request, call_next):
    return await HandleExceptions(request,call_next)

app.include_router(router)
