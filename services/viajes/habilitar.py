from config.db import SessionLocal
from models.viajes import Viajes
from sqlalchemy.exc import SQLAlchemyError


def habilitar_viaje_service(id_viaje: int):
    """
    Habilita un viaje actualizando su estado a True.
    Solo es posible habilitar viajes que están deshabilitados (estado=False).
    """
    db = SessionLocal()
    try:
        viaje = db.query(Viajes).filter(
            Viajes.id_viaje == id_viaje
        ).first()
        
        if not viaje:
            raise Exception(f"Viaje con ID {id_viaje} no encontrado")
        
        if viaje.estado:
            return {
                "success": False,
                "detail": "El viaje ya se encuentra habilitado."
            }
        
        viaje.estado = True
        
        db.commit()
        db.refresh(viaje)
        
        return {
            "success": True,
            "detail": f"El viaje '{viaje.nombre_viaje}' fue habilitado correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
