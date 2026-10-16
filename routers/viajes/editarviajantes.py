from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.viajes.editarviajantes import editar_viajantes_service
from schemas.viajes import EditarViajeRequest
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/viajes", 
    tags=["Viajes"]
)

security_scheme = HTTPBearer()


@router.put(
    "/editar-viajantes",
    dependencies=[Depends(require_role("PERMISO_CREAR_VIAJES_RENDICIONES"))]
)
async def editar_viajantes(
    request_body: EditarViajeRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    result = editar_viajantes_service(
        id_viaje=request_body.id_viaje,
        viajantes=request_body.viajantes
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result
