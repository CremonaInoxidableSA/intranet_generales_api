from config.db import SessionLocal
from models.viajes import Viajes
from models.monedas import Monedas
from sqlalchemy.exc import SQLAlchemyError


def editar_moneda_service(id_viaje: int, id_moneda: int):
    """
    Edita la moneda de un viaje existente.
    """
    db = SessionLocal()
    try:
        viaje = db.query(Viajes).filter(
            Viajes.id_viaje == id_viaje,
            Viajes.estado == True
        ).first()
        
        if not viaje:
            return {
                "success": False,
                "detail": "El viaje especificado no existe o no está activo."
            }
        
        moneda = db.query(Monedas).filter(
            Monedas.id_moneda == id_moneda,
            Monedas.estado == True
        ).first()
        
        if not moneda:
            return {
                "success": False,
                "detail": "La moneda especificada no existe o no está activa."
            }
        
        viaje.id_moneda = id_moneda
        db.commit()
        
        return {
            "success": True,
            "detail": f"La moneda del viaje se actualizó correctamente a '{moneda.nombre}'."
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()
