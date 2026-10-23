from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from security.dependencies import get_current_user
from services.tickets.pdf import validar_descarga_pdf
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

security_scheme = HTTPBearer()


@router.get("/descarga-pdf")
async def descargar_pdf(
    id_ticket: int = Query(..., description="ID del ticket"),
    current_user: AuthenticatedUser = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    """
    - PERMISO_VER_TICKETS_ADMIN_RENDICIONES: Acceso a cualquier PDF
    - PERMISO_VER_TICKETS_RENDICIONES: Solo a PDFs de sus propios viajes
    """
    permisos = getattr(current_user, 'roles', [])
    
    validacion = await validar_descarga_pdf(
        id_ticket=id_ticket,
        id_usuario=current_user.id,
        permisos_usuario=permisos
    )
    
    if not validacion["success"]:
        raise HTTPException(
            status_code=403,
            detail=validacion["detail"]
        )
    
    return FileResponse(
        path=validacion["ruta"],
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={validacion['nombre_archivo']}"}
    )
