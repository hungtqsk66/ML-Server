from fastapi import APIRouter
from Services.RecommendationService import ML_Model
from utils.ResponseTypes import SuccessResponse

model_controller = APIRouter(prefix='/model')
model = ML_Model()

@model_controller.get("/recommend")
async def get_recommend(id:str):
    return SuccessResponse(data = await model.recommend(id))