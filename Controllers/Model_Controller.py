from utils.ResponseTypes import SuccessResponse
from fastapi import APIRouter,Request,BackgroundTasks
from Services.RecommendationService import RecommendationService

model_controller = APIRouter(prefix='/model')
recommendationService =RecommendationService()

@model_controller.get("/recommend")
async def get_similarities(id:str):
    return SuccessResponse(await recommendationService.Recommend_Similarities(id))


@model_controller.get("/recommend/new")
async def get_NewRecommendation(request: Request,b_tasks:BackgroundTasks):
    user_id:str | None = request.headers.get("x-client-id")
    return SuccessResponse(await recommendationService.GetNewSongsRecommendation(user_id,b_tasks))
