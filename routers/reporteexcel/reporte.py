from fastapi import (APIRouter, HTTPException, Depends, Query)
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from security.permissions import require_role
from security.dependencies import get_current_user
from services.reporteexcel.reporte import generar_excel_tickets_service
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

security_scheme = HTTPBearer()


@router.get(
    "/excel/tickets",
    dependencies=[
        Depends(require_role("PERMISO_DESCARGAR_TICKETS_RENDICIONES")),
        Depends(get_current_user)
    ]
)
async def descargar_excel_tickets(
    id_viaje_usuario: int = Query(..., description="ID del viaje usuario"),
    current_user: AuthenticatedUser = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    result = await generar_excel_tickets_service(id_viaje_usuario=id_viaje_usuario)
    
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["detail"],
        )
    
    return StreamingResponse(
        iter([result["file"].getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=tickets_viaje_{id_viaje_usuario}.xlsx"}
    )
