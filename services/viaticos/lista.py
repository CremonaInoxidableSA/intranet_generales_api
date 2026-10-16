from config.db import SessionLocal
from models.viajes import Viajes
from sqlalchemy.exc import SQLAlchemyError


def listar_viajes_service():
    """
    Obtiene la lista de todos los viajes activos de la base de datos.
    """
    db = SessionLocal()
    try:
        viajes = db.query(Viajes).all()
        
        if not viajes:
            return {
                "success": True,
                "detail": "No hay viajes disponibles.",
                "data": []
            }
        
        viajes_list = [
            {
                "id_viaje": viaje.id_viaje,
                "nombre": viaje.nombre_viaje,
                "id_moneda": viaje.id_moneda,
                "moneda": viaje.moneda.nombre,
                "estado": viaje.estado
            }
            for viaje in viajes
        ]
        
        return {
            "success": True,
            "detail": "Viajes obtenidos correctamente.",
            "data": viajes_list
        }
    except SQLAlchemyError as e:
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()