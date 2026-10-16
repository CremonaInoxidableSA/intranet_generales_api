from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.medios_pago.crear import crear_medio_pago_service
from schemas.medios_pago import CrearMedioPagoRequest
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/medios-pago", 
    tags=["Medios Pago"]
)

security_scheme = HTTPBearer()


@router.post(
    "/crear",
    dependencies=[Depends(require_role("PERMISO_CREAR_MEDIOPAGO_RENDICIONES"))]
)
async def crear_medio_pago(
    request_body: CrearMedioPagoRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        result = crear_medio_pago_service(nombre=request_body.nombre)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
