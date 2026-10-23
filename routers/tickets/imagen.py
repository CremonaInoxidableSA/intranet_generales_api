from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os
import logging

from security.dependencies import get_current_user
from services.tickets.imagen import validar_acceso_imagen
from schemas.authenticated_user import AuthenticatedUser

logger = logging.getLogger(__name__)

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
    Permisos:
    - PERMISO_VER_TICKETS_ADMIN_RENDICIONES: Acceso a cualquier archivo
    - PERMISO_VER_TICKETS_RENDICIONES: Solo a archivos de sus propios viajes
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
    
    ruta_archivo = validacion["ruta"]
    extension = os.path.splitext(ruta_archivo)[1].lower()
    
    if extension in [".jpg", ".jpeg", ".png"]:
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png"
        }
        return FileResponse(
            ruta_archivo,
            media_type=media_types[extension],
            headers={"Content-Disposition": "inline"}
        )
    
    raiz_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    ruta_icono_pdf = os.path.join(raiz_proyecto, "imagenes", "utils", "PDF.png")
    
    if not os.path.exists(ruta_icono_pdf):
        raise HTTPException(
            status_code=404,
            detail=f"Ícono PDF no encontrado en: {ruta_icono_pdf}"
        )
    
    return FileResponse(
        ruta_icono_pdf,
        media_type="image/png",
        headers={"Content-Disposition": "inline"}
    )
