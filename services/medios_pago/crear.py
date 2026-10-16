from datetime import datetime
from config.db import SessionLocal
from models.medios_pago import MediosPago
from sqlalchemy.exc import SQLAlchemyError


def crear_medio_pago_service(nombre: str):
    """
    Crea un nuevo medio de pago en la base de datos.
    """
    if not nombre or not nombre.strip():
        raise ValueError("El nombre del medio de pago no puede estar vacío.")
    
    db = SessionLocal()
    try:
        nuevo_medio_pago = MediosPago(
            nombre=nombre.strip(),
            estado=True
        )
        
        db.add(nuevo_medio_pago)
        db.commit()
        db.refresh(nuevo_medio_pago)
        
        return {
            "success": True,
            "detail": f"Medio de pago '{nombre}' creado correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
