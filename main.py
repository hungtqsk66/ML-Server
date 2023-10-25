from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from middlewares.exeception_middleware import handle_exceptions
from middlewares.api_key_middleware import check_API_Key
from routers.recommend import model

app = FastAPI()
router = APIRouter(prefix="ml-server")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.middleware('http')
async def handle_request_middleware(request: Request, call_next):
    return await check_API_Key(request,call_next)

@app.middleware('http')
async def catch_exceptions_middleware(request: Request, call_next):
    return await handle_exceptions(request,call_next)

router.include_router(model.router)
app.include_router(router)