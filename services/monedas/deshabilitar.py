from config.db import SessionLocal
from models.monedas import Monedas
from sqlalchemy.exc import SQLAlchemyError


def deshabilitar_moneda_service(id_moneda: int):
    """
    Deshabilita una moneda actualizando su estado a False.
    Solo es posible deshabilitar monedas que están habilitadas (estado=True).
    """
    db = SessionLocal()
    try:
        moneda = db.query(Monedas).filter(
            Monedas.id_moneda == id_moneda
        ).first()
        
        if not moneda:
            raise Exception(f"Moneda con ID {id_moneda} no encontrada")
        
        if not moneda.estado:
            return {
                "success": False,
                "detail": "La moneda ya se encuentra deshabilitada."
            }
        
        moneda.estado = False
        
        db.commit()
        db.refresh(moneda)
        
        return {
            "success": True,
            "detail": f"La moneda '{moneda.nombre}' fue deshabilitada correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
