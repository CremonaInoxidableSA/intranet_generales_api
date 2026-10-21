from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from security.permissions import require_role
from security.dependencies import get_current_user
from services.tickets.eliminar import eliminar_ticket_service
from schemas.authenticated_user import AuthenticatedUser
from schemas.tickets import EliminarTicketRequest

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

security_scheme = HTTPBearer()


@router.delete(
    "/eliminar",
    dependencies=[
        Depends(require_role("PERMISO_ELIMINAR_TICKETS_RENDICIONES")),
        Depends(get_current_user)
    ]
)
async def eliminar_ticket(
    request: EliminarTicketRequest = Body(...),
    current_user: AuthenticatedUser = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    if not request.id_ticket:
        return {
            "success": False,
            "detail": "El id_ticket es requerido"
        }
    
    result = await eliminar_ticket_service(
        id_ticket=request.id_ticket,
        id_usuario_jwt=current_user.id
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["detail"],
        )
    
    return result
