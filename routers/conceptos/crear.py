from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.conceptos.crear import crear_concepto_service
from schemas.conceptos import CrearConceptoRequest
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/conceptos", 
    tags=["Conceptos"]
)

security_scheme = HTTPBearer()


@router.post(
    "/crear",
    dependencies=[Depends(require_role("PERMISO_CREAR_CONCEPTO_RENDICIONES"))]
)
async def crear_concepto(
    request_body: CrearConceptoRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        result = crear_concepto_service(nombre=request_body.nombre)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
