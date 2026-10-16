from pydantic import BaseModel
from typing import List


class CrearViajeRequest(BaseModel):
    nombre_viaje: str
    id_moneda: int


class ViajanteMixin(BaseModel):
    id_usuario_viajante: str
    nombre_usuario_viajante: str
    apellido_usuario_viajante: str
    legajo_usuario_viajante: str


class EditarViajeRequest(BaseModel):
    id_viaje: int
    viajantes: List[ViajanteMixin]


class HabilitarViajeRequest(BaseModel):
    """Schema para la solicitud de habilitación de viaje"""
    id_viaje: int


class DeshabilitarViajeRequest(BaseModel):
    """Schema para la solicitud de deshabilitación de viaje"""
    id_viaje: int


class EditarMonedaViajeRequest(BaseModel):
    """Schema para la solicitud de edición de moneda de un viaje"""
    id_viaje: int
    id_moneda: int