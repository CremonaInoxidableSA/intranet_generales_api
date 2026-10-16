from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class ViajeUsuario(Base):
    __tablename__ = "viaje_usuario"

    id_viaje_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_viaje = Column(Integer, ForeignKey("viajes.id_viaje"), nullable=False)
    id_usuario_viajante = Column(String(255), nullable=False)
    nombre_usuario_viajante = Column(String(255), nullable=False)
    apellido_usuario_viajante = Column(String(255), nullable=False)
    legajo_usuario_viajante = Column(String(255), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)

    viaje = relationship("Viajes", back_populates="viaje_usuarios")
    comentarios = relationship("Comentarios", back_populates="viaje_usuario")
    tickets = relationship("TicketUsuario", back_populates="viaje_usuario")
    viaticos = relationship("Viaticos", back_populates="viaje_usuario")