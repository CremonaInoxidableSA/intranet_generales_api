from pydantic import BaseModel
from datetime import date


class CargarTicketsRequest(BaseModel):
    id_viaje_usuario: int


class EditarTicketRequest(BaseModel):
    id_ticket: int
    nombre_imagen: str
    monto: int
    fecha_gasto: date
    id_medio_pago: int
    id_moneda: int
    id_concepto: int

class AprobarTicketRequest(BaseModel):
    id_ticket: int