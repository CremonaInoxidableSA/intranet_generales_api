from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.viajes.detalles import obtener_detalles_viaje_service
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/viajes", 
    tags=["Viajes"]
)

security_scheme = HTTPBearer()


@router.get(
    "/detalles",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_DETALLESVIAJES_RENDICIONES"))]
)
async def obtener_detalles_viaje(
    id_viaje: int,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    result = obtener_detalles_viaje_service(id_viaje)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result
