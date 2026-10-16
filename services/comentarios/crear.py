from datetime import datetime
from config.db import SessionLocal
from models.comentarios import Comentarios
from models.viaje_usuario import ViajeUsuario
from sqlalchemy.exc import SQLAlchemyError


def crear_comentario_service(
    id_viaje_usuario: int,
    id_usuario_creador: str,
    nombre_usuario_creador: str,
    apellido_usuario_creador: str,
    comentario: str
):
    """
    Crea un nuevo comentario en la base de datos.
    """
    if not comentario or not comentario.strip():
        return {
            "success": False,
            "detail": "El comentario no puede estar vacío."
        }
    
    db = SessionLocal()
    try:
        # Validar que el viaje_usuario existe
        viaje_usuario = db.query(ViajeUsuario).filter(
            ViajeUsuario.id_viaje_usuario == id_viaje_usuario
        ).first()
        
        if not viaje_usuario:
            return {
                "success": False,
                "detail": "El viaje para este usuario no existe."
            }
        
        if viaje_usuario.estado == False:
            return {
                "success": False,
                "detail": "El viaje para este usuario no está activo."
            }

        # Crear el nuevo comentario
        nuevo_comentario = Comentarios(
            id_viaje_usuario=id_viaje_usuario,
            id_usuario_creador=id_usuario_creador,
            nombre_usuario_creador=nombre_usuario_creador,
            apellido_usuario_creador=apellido_usuario_creador,
            fecha_creacion=datetime.now(),
            comentario=comentario.strip()
        )
        
        db.add(nuevo_comentario)
        db.commit()
        db.refresh(nuevo_comentario)
        
        return {
            "success": True,
            "detail": "Comentario creado correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()
