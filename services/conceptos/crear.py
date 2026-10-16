from datetime import datetime
from config.db import SessionLocal
from models.conceptos import Conceptos
from sqlalchemy.exc import SQLAlchemyError


def crear_concepto_service(nombre: str):
    """
    Crea un nuevo concepto en la base de datos.
    """
    if not nombre or not nombre.strip():
        raise ValueError("El nombre del concepto no puede estar vacío.")
    
    db = SessionLocal()
    try:
        nuevo_concepto = Conceptos(
            nombre=nombre.strip(),
            estado=True
        )
        
        db.add(nuevo_concepto)
        db.commit()
        db.refresh(nuevo_concepto)
        
        return {
            "success": True,
            "detail": f"Concepto '{nombre}' creado correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
