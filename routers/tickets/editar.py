from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from security.permissions import require_role
from security.dependencies import get_current_user
from services.tickets.editar import editar_ticket_service
from schemas.authenticated_user import AuthenticatedUser
from schemas.tickets import EditarTicketRequest

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

security_scheme = HTTPBearer()


@router.put(
    "/editar",
    dependencies=[
        Depends(require_role("PERMISO_EDITAR_TICKETS_RENDICIONES")),
        Depends(get_current_user)
    ]
)
async def editar_ticket(
    request: EditarTicketRequest = Body(...),
    current_user: AuthenticatedUser = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    if not all([
        request.id_ticket,
        request.nombre_imagen,
        request.monto,
        request.fecha_gasto,
        request.id_medio_pago,
        request.id_moneda,
        request.id_concepto
    ]):
        return {
            "success": False,
            "detail": "Todos los campos deben estar completos"
        }
    
    result = await editar_ticket_service(
        id_ticket=request.id_ticket,
        nombre_imagen=request.nombre_imagen,
        monto=request.monto,
        fecha_gasto=request.fecha_gasto,
        id_medio_pago=request.id_medio_pago,
        id_moneda=request.id_moneda,
        id_concepto=request.id_concepto,
        id_usuario_jwt=current_user.id
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["detail"],
        )
    
    return result
