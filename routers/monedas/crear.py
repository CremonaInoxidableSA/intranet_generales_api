from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.permissions import require_role
from security.dependencies import get_current_user
from services.monedas.crear import crear_moneda_service
from schemas.monedas import CrearMonedaRequest
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/monedas", 
    tags=["Monedas"]
)

security_scheme = HTTPBearer()


@router.post(
    "/crear",
    dependencies=[Depends(require_role("PERMISO_CREAR_MONEDA_RENDICIONES"))]
)
async def crear_moneda(
    request_body: CrearMonedaRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        result = crear_moneda_service(nombre=request_body.nombre)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
