from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.viaticos.crear import crear_viaticos_service
from schemas.viaticos import CrearViaticosRequest
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/viaticos", 
    tags=["Viaticos"]
)

security_scheme = HTTPBearer()


@router.post(
    "/crear",
    dependencies=[Depends(require_role("PERMISO_CREAR_VIATICOS_RENDICIONES"))]
)
async def crear_viatico(
    request_body: CrearViaticosRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    result = crear_viaticos_service(
        id_viaje_usuario=request_body.id_viaje_usuario,
        id_usuario_viajante=current_user.id,
        id_moneda=request_body.id_moneda,
        monto_entregado=request_body.monto_entregado,
        monto_devuelto=request_body.monto_devuelto
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result
