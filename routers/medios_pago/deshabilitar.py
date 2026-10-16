from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.medios_pago.deshabilitar import deshabilitar_mediopago_service
from schemas.authenticated_user import AuthenticatedUser
from schemas.medios_pago import DeshabilitarMedioPagoRequest

router = APIRouter(
    prefix="/medios-pago", 
    tags=["Medios Pago"]
)

security_scheme = HTTPBearer()

@router.post(
    "/deshabilitar",
    dependencies=[Depends(require_role("PERMISO_ESTADOS_MEDIOPAGO_RENDICIONES"))]
)
async def deshabilitar_mediopago(
    request_body: DeshabilitarMedioPagoRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Deshabilita un medio de pago.
    Requiere permiso: PERMISO_ESTADOS_MEDIOPAGO_RENDICIONES
    """
    try:
        resultado = deshabilitar_mediopago_service(request_body.id_medio_pago)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
