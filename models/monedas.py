from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from config.db import Base

class Monedas(Base):
    __tablename__ = "monedas"

    id_moneda = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    
    viajes = relationship("Viajes", back_populates="moneda")
    tickets = relationship("TicketUsuario", back_populates="moneda")
    viaticos = relationship("Viaticos", back_populates="moneda")