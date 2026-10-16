from pydantic import BaseModel
from typing import Optional


class CrearMonedaRequest(BaseModel):
    """Schema para la solicitud de creación de moneda"""
    nombre: str


class HabilitarMonedaRequest(BaseModel):
    """Schema para la solicitud de habilitación de moneda"""
    id_moneda: int


class DeshabilitarMonedaRequest(BaseModel):
    """Schema para la solicitud de deshabilitación de moneda"""
    id_moneda: int


class MonedaResponse(BaseModel):
    """Schema para la respuesta de una moneda"""
    id_moneda: int
    nombre: str
    estado: bool

    class Config:
        from_attributes = True