from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from security.dependencies import get_current_user
from services.tickets.imagen import validar_acceso_imagen
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

security_scheme = HTTPBearer()


@router.get("/imagen")
async def obtener_imagen(
    id_ticket: int = Query(..., description="ID del ticket"),
    current_user: AuthenticatedUser = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    """
    Obtener imagen con validación de permisos y propiedad.
    
    - PERMISO_VER_TICKETS_ADMIN_RENDICIONES: Acceso a cualquier imagen
    - PERMISO_VER_TICKETS_RENDICIONES: Solo a imágenes de sus propios viajes
    """
    permisos = getattr(current_user, 'roles', [])
    
    validacion = await validar_acceso_imagen(
        id_ticket=id_ticket,
        id_usuario=current_user.id,
        permisos_usuario=permisos
    )
    
    if not validacion["success"]:
        raise HTTPException(
            status_code=403,
            detail=validacion["detail"]
        )
    
    return FileResponse(validacion["ruta"])
