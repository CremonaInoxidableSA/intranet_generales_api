from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.viajes.lista import listar_viajes_service
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/viajes", 
    tags=["Viajes"]
)

security_scheme = HTTPBearer()


@router.get(
    "/lista",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_VIAJES_RENDICIONES"))]
)
async def listar_viajes(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        result = listar_viajes_service()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
