from fastapi import (APIRouter, HTTPException, Depends, Query)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from security.permissions import require_role
from security.dependencies import get_current_user
from services.tickets.lista import listar_tickets_service
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

security_scheme = HTTPBearer()


@router.get(
    "/lista",
    dependencies=[
        Depends(require_role("PERMISO_VER_TICKETS_RENDICIONES")),
        Depends(get_current_user)
    ]
)
async def listar_tickets(
    id_viaje_usuario: int = Query(..., description="ID del viaje usuario"),
    current_user: AuthenticatedUser = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    result = await listar_tickets_service(id_viaje_usuario=id_viaje_usuario)
    
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["detail"],
        )
    
    return result
