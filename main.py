from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from middlewares.exeception_middleware import handle_exceptions
from middlewares.api_key_middleware import check_API_Key
from routers.recommend import model


router = APIRouter(prefix='/api/ml-server')

router.include_router(model.router)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nth-audio.site","http://127.0.0.1:5500"],
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

@app.get("/")
def get():return {"msg":"hello"}
app.include_router(router)