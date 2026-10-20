from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class TicketUsuario(Base):
    __tablename__ = "ticket_usuario"

    id_ticket = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_viaje_usuario = Column(Integer, ForeignKey("viaje_usuario.id_viaje_usuario"), nullable=False)
    fecha_carga = Column(DateTime, nullable=False)
    fecha_gasto = Column(DateTime, nullable=True)
    nombre_imagen = Column(String(255), nullable=False)
    monto = Column(Integer, nullable=True)
    id_medio_pago = Column(Integer, ForeignKey("medios_pago.id_medio_pago"), nullable=True)
    id_moneda = Column(Integer, ForeignKey("monedas.id_moneda"), nullable=True)
    id_concepto = Column(Integer, ForeignKey("conceptos.id_concepto"), nullable=True)
    estado_ticket_usuario = Column(String(255), nullable=False)
    estado_ticket_admin = Column(String(255), nullable=True)
    
    viaje_usuario = relationship("ViajeUsuario", back_populates="tickets")
    medio_pago = relationship("MediosPago", back_populates="tickets")
    moneda = relationship("Monedas", back_populates="tickets")
    concepto = relationship("Conceptos", back_populates="tickets")