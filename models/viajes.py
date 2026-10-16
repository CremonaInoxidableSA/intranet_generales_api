from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Viajes(Base):
    __tablename__ = "viajes"

    id_viaje = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_viaje = Column(String(255), nullable=False)
    id_moneda = Column(Integer, ForeignKey("monedas.id_moneda"), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    
    moneda = relationship("Monedas", back_populates="viajes")
    viaje_usuarios = relationship("ViajeUsuario", back_populates="viaje")