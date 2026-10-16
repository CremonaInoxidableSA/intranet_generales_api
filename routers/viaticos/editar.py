from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.viaticos.editar import editar_viaticos_service
from schemas.viaticos import EditarViaticosRequest
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/viaticos", 
    tags=["Viaticos"]
)

security_scheme = HTTPBearer()


@router.put(
    "/editar",
    dependencies=[Depends(require_role("PERMISO_EDITAR_VIATICOS_RENDICIONES"))]
)
async def editar_viatico(
    request_body: EditarViaticosRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    result = editar_viaticos_service(
        id_viatico=request_body.id_viatico,
        id_usuario_viajante=current_user.id,
        id_moneda=request_body.id_moneda,
        monto_entregado=request_body.monto_entregado,
        monto_devuelto=request_body.monto_devuelto
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result
