from pydantic import BaseModel


class CargarTicketsRequest(BaseModel):
    id_viaje_usuario: int
