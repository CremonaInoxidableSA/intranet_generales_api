from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Viaticos(Base):
    __tablename__ = "viaticos"

    id_viatico = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_viaje_usuario = Column(Integer, ForeignKey("viaje_usuario.id_viaje_usuario"), nullable=False)
    id_moneda = Column(Integer, ForeignKey("monedas.id_moneda"), nullable=False)
    monto_entregado = Column(Integer, nullable=False)
    monto_devuelto = Column(Integer, nullable=True)
    estado = Column(Boolean, nullable=False, default=False)
    
    viaje_usuario = relationship("ViajeUsuario", back_populates="viaticos")
    moneda = relationship("Monedas", back_populates="viaticos")