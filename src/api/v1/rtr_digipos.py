from typing import Annotated

from fastapi import APIRouter, Query
from src.deps import DigiposRepoDep
from src.domain.digipos.sch_request import ReqBalance, ResReqBalance

router = APIRouter(prefix="/digipos", tags=["Digipos"])


@router.get(
    path="/balance",
    summary="Get balance from Digipos API",
    description="pastikan username itu sesuai dengan digipos dan sudah di daftarkan di settings.",
    response_model=ResReqBalance,
)
async def get_balance_digipos(
    repo: DigiposRepoDep, payload: Annotated[ReqBalance, Query()]
):
    """Endpoint untuk mendapatkan saldo pengguna dari Digipos API."""
    response = await repo.get_balance(username=payload.username)
    return response
