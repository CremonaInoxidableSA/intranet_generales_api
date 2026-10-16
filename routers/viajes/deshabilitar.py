from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.viajes.deshabilitar import deshabilitar_viaje_service
from schemas.authenticated_user import AuthenticatedUser
from schemas.viajes import DeshabilitarViajeRequest

router = APIRouter(
    prefix="/viajes", 
    tags=["Viajes"]
)

security_scheme = HTTPBearer()


@router.post(
    "/deshabilitar",
    dependencies=[Depends(require_role("PERMISO_ESTADOS_VIAJES_RENDICIONES"))]
)
async def deshabilitar_viaje(
    request_body: DeshabilitarViajeRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Deshabilita un viaje.
    Requiere permiso: PERMISO_ESTADOS_VIAJES_RENDICIONES
    """
    try:
        resultado = deshabilitar_viaje_service(request_body.id_viaje)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
