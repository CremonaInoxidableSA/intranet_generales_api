from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.conceptos.deshabilitar import deshabilitar_concepto_service
from schemas.authenticated_user import AuthenticatedUser
from schemas.conceptos import DeshabilitarConceptoRequest

router = APIRouter(
    prefix="/conceptos", 
    tags=["Conceptos"]
)

security_scheme = HTTPBearer()

@router.post(
    "/deshabilitar",
    dependencies=[Depends(require_role("PERMISO_ESTADOS_CONCEPTOS_RENDICIONES"))]
)
async def deshabilitar_concepto(
    request_body: DeshabilitarConceptoRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Deshabilita un concepto.
    Requiere permiso: PERMISO_ESTADOS_CONCEPTOS_RENDICIONES
    """
    try:
        resultado = deshabilitar_concepto_service(request_body.id_concepto)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
