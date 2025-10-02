from fastapi import APIRouter
from src.deps import DigiposRepoDep, HttpClientDep

router = APIRouter(prefix="/digipos", tags=["Digipos"])


@router.get("/login")
async def login_digipos(client: HttpClientDep):
    """Endpoint untuk login ke Digipos API."""
    return {"message": "Login successful"}


@router.get("/profile")
async def get_profile_digipos(repo: DigiposRepoDep):
    """Endpoint untuk mendapatkan profil pengguna dari Digipos API."""


@router.get("/balance")
async def get_balance_digipos(repo: DigiposRepoDep):
    """Endpoint untuk mendapatkan saldo pengguna dari Digipos API."""
    username = repo.config.api.username
    response = await repo.get_balance(username)
    return response.json()


@router.get("/logout")
async def logout_digipos():
    """Endpoint untuk logout dari Digipos API."""
    return {"message": "Logout successful"}
