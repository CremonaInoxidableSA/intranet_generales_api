from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.viaticos.aprobar import aprobar_viaticos_service
from schemas.viaticos import AprobarViaticosRequest
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/viaticos", 
    tags=["Viaticos"]
)

security_scheme = HTTPBearer()


@router.put(
    "/aprobar",
    dependencies=[Depends(require_role("PERMISO_APROBAR_VIATICOS_RENDICIONES"))]
)
async def aprobar_viatico(
    request_body: AprobarViaticosRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    result = aprobar_viaticos_service(id_viatico=request_body.id_viatico)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result
