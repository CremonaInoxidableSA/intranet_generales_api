from pydantic import BaseModel


class CrearViaticosRequest(BaseModel):
    id_viaje_usuario: int
    id_moneda: int
    monto_entregado: int
    monto_devuelto: int | None = None


class EditarViaticosRequest(BaseModel):
    id_viatico: int
    id_moneda: int
    monto_entregado: int
    monto_devuelto: int | None = None


class AprobarViaticosRequest(BaseModel):
    id_viatico: int
