from fastapi import FastAPI,APIRouter,Request
from starlette.middleware.cors import CORSMiddleware 
from middlewares.ExceptionHandler import HandleExceptions
from middlewares.AuthorizeRequests import AuthorizeAccess
from Controllers.Model_Controller import model_controller


router = APIRouter(prefix='/api/ml-server')
router.include_router(model_controller)
app = FastAPI()

@app.middleware('http')
async def AuthorizeRequest_Middleware(request: Request, call_next):
    return await AuthorizeAccess(request,call_next)

@app.middleware('http')      
async def ExceptionHandling_Middleware(request: Request, call_next):
    return await HandleExceptions(request,call_next)

app.include_router(router)

#Must move cors middleware to the end of app to make it work behind proxy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)