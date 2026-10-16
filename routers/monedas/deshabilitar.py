from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.monedas.deshabilitar import deshabilitar_moneda_service
from schemas.authenticated_user import AuthenticatedUser
from schemas.monedas import DeshabilitarMonedaRequest

router = APIRouter(
    prefix="/monedas", 
    tags=["Monedas"]
)

security_scheme = HTTPBearer()


@router.post(
    "/deshabilitar",
    dependencies=[Depends(require_role("PERMISO_ESTADOS_MONEDA_RENDICIONES"))]
)
async def deshabilitar_moneda(
    request_body: DeshabilitarMonedaRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Deshabilita una moneda.
    Requiere permiso: PERMISO_ESTADOS_MONEDA_RENDICIONES
    """
    try:
        resultado = deshabilitar_moneda_service(request_body.id_moneda)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
