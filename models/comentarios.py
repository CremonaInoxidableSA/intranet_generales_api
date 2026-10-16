from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Comentarios(Base):
    __tablename__ = "comentarios"

    id_comentario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_viaje_usuario = Column(Integer, ForeignKey("viaje_usuario.id_viaje_usuario"), nullable=False)
    id_usuario_creador = Column(String(255), nullable=False)
    nombre_usuario_creador = Column(String(255), nullable=False)
    apellido_usuario_creador = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    comentario = Column(String(255), nullable=False)
    
    viaje_usuario = relationship("ViajeUsuario", back_populates="comentarios")