from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from utils.Response.response_types import ErrorResponse
from routers.recommend import model


router = APIRouter(prefix='/api/ml-server')

router.include_router(model.router)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware('http')
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except:
        return ErrorResponse()


app.include_router(router)


