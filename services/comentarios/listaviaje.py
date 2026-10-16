from config.db import SessionLocal
from models.comentarios import Comentarios
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc


def listar_comentarios_por_viaje_service(id_viaje_usuario: int):
    """
    Obtiene la lista de comentarios de un viaje_usuario específico.
    Ordena por fecha de creación descendente (más recientes primero).
    """
    db = SessionLocal()
    try:
        comentarios = db.query(Comentarios).filter(
            Comentarios.id_viaje_usuario == id_viaje_usuario
        ).order_by(desc(Comentarios.fecha_creacion)).all()
        
        if not comentarios:
            return {
                "success": True,
                "detail": "No hay comentarios disponibles para este viaje.",
                "data": []
            }
        
        comentarios_list = [
            {
                "nombre_usuario_creador": comentario.nombre_usuario_creador,
                "apellido_usuario_creador": comentario.apellido_usuario_creador,
                "comentario": comentario.comentario,
                "fecha_creacion": comentario.fecha_creacion
            }
            for comentario in comentarios
        ]
        
        return {
            "success": True,
            "detail": "Comentarios obtenidos correctamente.",
            "data": comentarios_list
        }
    except SQLAlchemyError as e:
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()
