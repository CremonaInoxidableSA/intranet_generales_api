from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.monedas.habilitar import habilitar_moneda_service
from schemas.authenticated_user import AuthenticatedUser
from schemas.monedas import HabilitarMonedaRequest

router = APIRouter(
    prefix="/monedas", 
    tags=["Monedas"]
)

security_scheme = HTTPBearer()


@router.post(
    "/habilitar",
    dependencies=[Depends(require_role("PERMISO_ESTADOS_MONEDA_RENDICIONES"))]
)
async def habilitar_moneda(
    request_body: HabilitarMonedaRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Habilita una moneda.
    Requiere permiso: PERMISO_ESTADOS_MONEDA_RENDICIONES
    """
    try:
        resultado = habilitar_moneda_service(request_body.id_moneda)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
