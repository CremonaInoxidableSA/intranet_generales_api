from pydantic import BaseModel


class CrearComentarioRequest(BaseModel):
    id_viaje_usuario: int
    comentario: str
