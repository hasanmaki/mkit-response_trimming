from fastapi import APIRouter
from src.deps import DigiposRepoDep

router = APIRouter(prefix="/digipos", tags=["Digipos"])


@router.get("/balance")
async def get_balance(repos: DigiposRepoDep):
    username = repos.config.api.username
    balance_data = await repos.get_balance(username=username)
    return balance_data
