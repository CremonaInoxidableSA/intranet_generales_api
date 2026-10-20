from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from security.permissions import require_role
from security.dependencies import get_current_user
from services.tickets.detalles import obtener_detalles_ticket_service
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

security_scheme = HTTPBearer()


@router.get(
    "/detalles",
    dependencies=[
        Depends(require_role("PERMISO_VER_TICKETS_RENDICIONES")),
        Depends(get_current_user)
    ]
)
async def obtener_detalles_ticket(
    id_ticket: int = Query(..., description="ID del ticket"),
    current_user: AuthenticatedUser = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    permisos = getattr(current_user, 'roles', [])
    
    result = await obtener_detalles_ticket_service(
        id_ticket=id_ticket,
        id_usuario_jwt=current_user.id,
        permisos_usuario=permisos
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["detail"],
        )
    
    return result
