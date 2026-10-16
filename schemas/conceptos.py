from pydantic import BaseModel
from typing import Optional


class CrearConceptoRequest(BaseModel):
    """Schema para la solicitud de creación de concepto"""
    nombre: str

class HabilitarConceptoRequest(BaseModel):
    """Schema para la solicitud de habilitación de concepto"""
    id_concepto: int


class DeshabilitarConceptoRequest(BaseModel):
    """Schema para la solicitud de deshabilitación de concepto"""
    id_concepto: int


class ConceptoResponse(BaseModel):
    """Schema para la respuesta de un concepto"""
    id_concepto: int
    nombre: str
    estado: bool

    class Config:
        from_attributes = True