from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from config.db import Base

class Conceptos(Base):
    __tablename__ = "conceptos"

    id_concepto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    
    tickets = relationship("TicketUsuario", back_populates="concepto")