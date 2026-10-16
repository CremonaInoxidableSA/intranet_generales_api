from pydantic import BaseModel
from typing import Optional


class CrearMedioPagoRequest(BaseModel):
    """Schema para la solicitud de creación de medio de pago"""
    nombre: str

class HabilitarMedioPagoRequest(BaseModel):
    """Schema para la solicitud de habilitación de medio de pago"""
    id_medio_pago: int


class DeshabilitarMedioPagoRequest(BaseModel):
    """Schema para la solicitud de deshabilitación de medio de pago"""
    id_medio_pago: int


class MedioPagoResponse(BaseModel):
    """Schema para la respuesta de un medio de pago"""
    id_medio_pago: int
    nombre: str
    estado: bool

    class Config:
        from_attributes = True