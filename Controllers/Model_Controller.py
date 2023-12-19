from fastapi import APIRouter,Request,BackgroundTasks
from Services.RecommendationService import ModelService
from utils.ResponseTypes import SuccessResponse

model_controller = APIRouter(prefix='/model')
model =ModelService()

@model_controller.get("/recommend")
async def get_similarities(id:str):
    return SuccessResponse(await model.Recommend_Similarities(id))


@model_controller.get("/recommend/new")
async def get_NewRecommendation(request: Request,b_tasks:BackgroundTasks):
    user_id:str | None = request.headers.get("x-client-id")
    return SuccessResponse(await model.Recommend_NewSongsBased(user_id,b_tasks))
