from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.comentarios.crear import crear_comentario_service
from schemas.comentarios import CrearComentarioRequest
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/comentarios", 
    tags=["Comentarios"]
)

security_scheme = HTTPBearer()


@router.post(
    "/crear",
    dependencies=[Depends(require_role("PERMISO_CREAR_COMENTARIO_RENDICIONES"))]
)
async def crear_comentario(
    request_body: CrearComentarioRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    result = crear_comentario_service(
        id_viaje_usuario=request_body.id_viaje_usuario,
        id_usuario_creador=current_user.id,
        nombre_usuario_creador=current_user.first_name or "",
        apellido_usuario_creador=current_user.last_name or "",
        comentario=request_body.comentario
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result
