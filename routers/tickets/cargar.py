from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    UploadFile,
    File,
    Query,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from security.permissions import require_role
from security.dependencies import get_current_user
from services.tickets.cargar import cargar_tickets_service
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

security_scheme = HTTPBearer()


@router.post(
    "/cargar-tickets",
    dependencies=[
        Depends(require_role("PERMISO_CREAR_TICKETS_RENDICIONES")),
        Depends(get_current_user)
    ]
)
async def cargar_tickets(
    archivos: list[UploadFile],
    id_viaje_usuario: int = Query(..., description="ID del viaje usuario"),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    result = await cargar_tickets_service(
        id_viaje_usuario=id_viaje_usuario,
        archivos=archivos,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["detail"],
        )

    return result