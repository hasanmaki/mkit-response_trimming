from fastapi import APIRouter
from src.deps import DigiposServiceDep

router = APIRouter(prefix="/digipos", tags=["Digipos"])


@router.get("/balance")
async def get_balance(service: DigiposServiceDep):
    balance_data = await service.get_balance()
    return balance_data
