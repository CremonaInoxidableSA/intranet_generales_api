from datetime import datetime
from config.db import SessionLocal
from models.monedas import Monedas
from sqlalchemy.exc import SQLAlchemyError


def crear_moneda_service(nombre: str):
    """
    Crea una nueva moneda en la base de datos.
    """
    if not nombre or not nombre.strip():
        raise ValueError("El nombre de la moneda no puede estar vacío.")
    
    db = SessionLocal()
    try:
        nueva_moneda = Monedas(
            nombre=nombre.strip(),
            estado=True
        )
        
        db.add(nueva_moneda)
        db.commit()
        db.refresh(nueva_moneda)
        
        return {
            "success": True,
            "detail": f"Moneda '{nombre}' creada correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
