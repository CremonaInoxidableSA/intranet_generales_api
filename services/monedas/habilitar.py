from config.db import SessionLocal
from models.monedas import Monedas
from sqlalchemy.exc import SQLAlchemyError


def habilitar_moneda_service(id_moneda: int):
    """
    Habilita una moneda actualizando su estado a True.
    Solo es posible habilitar monedas que están deshabilitadas (estado=False).
    """
    db = SessionLocal()
    try:
        moneda = db.query(Monedas).filter(
            Monedas.id_moneda == id_moneda
        ).first()
        
        if not moneda:
            raise Exception(f"Moneda con ID {id_moneda} no encontrada")
        
        if moneda.estado:
            return {
                "success": False,
                "detail": "La moneda ya se encuentra habilitada."
            }
        
        moneda.estado = True
        
        db.commit()
        db.refresh(moneda)
        
        return {
            "success": True,
            "detail": f"La moneda '{moneda.nombre}' fue habilitada correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
