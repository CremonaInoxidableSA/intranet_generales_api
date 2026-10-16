from config.db import SessionLocal
from models.viajes import Viajes
from sqlalchemy.exc import SQLAlchemyError


def deshabilitar_viaje_service(id_viaje: int):
    """
    Deshabilita un viaje actualizando su estado a False.
    Solo es posible deshabilitar viajes que están habilitados (estado=True).
    """
    db = SessionLocal()
    try:
        viaje = db.query(Viajes).filter(
            Viajes.id_viaje == id_viaje
        ).first()
        
        if not viaje:
            raise Exception(f"Viaje con ID {id_viaje} no encontrado")
        
        if not viaje.estado:
            return {
                "success": False,
                "detail": "El viaje ya se encuentra deshabilitado."
            }
        
        viaje.estado = False
        
        db.commit()
        db.refresh(viaje)
        
        return {
            "success": True,
            "detail": f"El viaje '{viaje.nombre_viaje}' fue deshabilitado correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
