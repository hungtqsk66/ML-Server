from utils.ResponseTypes import SuccessResponse,ErrorResponse
from fastapi import APIRouter,Request,BackgroundTasks,status
from Services.RecommendationService import RecommendationService
from Services.DBService import DBService

model_controller = APIRouter(prefix='/model')
recommendationService =RecommendationService()
dbService = DBService()

@model_controller.get("/recommend")
async def get_similarities(id:str):
    return SuccessResponse(await recommendationService.Recommend_Similarities(id))


@model_controller.get("/recommend/new")
async def get_NewRecommendation(request: Request,b_tasks:BackgroundTasks):
    user_id:str | None = request.headers.get("x-client-id")
    accessToken:str | None = request.headers.get("authorization")
    isAuthorize:bool = await dbService.ValidateAccessToken(user_id,accessToken)
    if not isAuthorize: return ErrorResponse(message="Unauthorized",code=status.HTTP_401_UNAUTHORIZED)
    return SuccessResponse(await recommendationService.GetNewSongsRecommendation(user_id,b_tasks))
