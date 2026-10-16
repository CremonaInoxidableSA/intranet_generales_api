from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.medios_pago.lista import listar_mediospago_service
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/medios-pago", 
    tags=["Medios Pago"]
)

security_scheme = HTTPBearer()


@router.get(
    "/lista",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_MEDIOPAGO_RENDICIONES"))]
)
async def listar_mediospago(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        result = listar_mediospago_service()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
