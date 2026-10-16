from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.viajes.editarmoneda import editar_moneda_service
from schemas.viajes import EditarMonedaViajeRequest
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/viajes", 
    tags=["Viajes"]
)

security_scheme = HTTPBearer()


@router.put(
    "/editar-moneda",
    dependencies=[Depends(require_role("PERMISO_CREAR_VIAJES_RENDICIONES"))]
)
async def editar_moneda(
    request_body: EditarMonedaViajeRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    result = editar_moneda_service(
        id_viaje=request_body.id_viaje,
        id_moneda=request_body.id_moneda
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result
