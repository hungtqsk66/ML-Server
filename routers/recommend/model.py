from fastapi import APIRouter
from services.recommend.ml_recommend import ML_Model

router = APIRouter(prefix='/model')
model = ML_Model()

@router.get("/recommend")
async def get_recommend(id:str):
    return await model.recommend(id)