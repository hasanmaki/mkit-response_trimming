from fastapi import APIRouter, Depends

from deps import get_digipos_service
from services.digipos.srv_digipos import DigiposService

router = APIRouter(prefix="/digipos", tags=["Digipos"])


@router.get("/balance")
async def get_balance(digipos_service: DigiposService = Depends(get_digipos_service)):
    """Endpoint untuk mengambil saldo dari Digipos API."""
    # DigiposServiceDep sudah menjamin client dan config sudah terinject ke service
    result = await digipos_service.get_balance()
    return {"status": "success", "data": result}
