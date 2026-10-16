from config.db import SessionLocal
from models.viajes import Viajes
from sqlalchemy.exc import SQLAlchemyError


def obtener_detalles_viaje_service(id_viaje: int):
    """
    Obtiene los detalles de un viaje específico.
    """
    db = SessionLocal()
    try:
        viaje = db.query(Viajes).filter(
            Viajes.id_viaje == id_viaje
        ).first()
        
        if not viaje:
            return {
                "success": False,
                "detail": "El viaje especificado no existe."
            }
        
        viajantes = [
            {
                "id_usuario_viajante": viaje_usuario.id_usuario_viajante,
                "nombre_usuario_viajante": viaje_usuario.nombre_usuario_viajante,
                "apellido_usuario_viajante": viaje_usuario.apellido_usuario_viajante,
                "legajo_usuario_viajante": viaje_usuario.legajo_usuario_viajante
            }
            for viaje_usuario in viaje.viaje_usuarios
            if viaje_usuario.estado == True
        ]
        
        return {
            "success": True,
            "detail": "Detalles del viaje obtenidos correctamente.",
            "data": {
                "id_viaje": viaje.id_viaje,
                "nombre_viaje": viaje.nombre_viaje,
                "moneda_nombre": viaje.moneda.nombre,
                "viajantes": viajantes
            }
        }
    except SQLAlchemyError as e:
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()