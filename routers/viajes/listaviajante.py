from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.viajes.listaviajante import listar_viajes_por_viajante_service
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/viajes", 
    tags=["Viajes"]
)

security_scheme = HTTPBearer()


@router.get(
    "/viajante",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_VIAJESPERSONALES_RENDICIONES"))]
)
async def listar_viajes_por_viajante(
    id_usuario_viajante: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    result = listar_viajes_por_viajante_service(id_usuario_viajante=id_usuario_viajante)
    
    return result
