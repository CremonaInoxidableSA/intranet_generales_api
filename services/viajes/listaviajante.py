from config.db import SessionLocal
from models.viaje_usuario import ViajeUsuario
from models.viajes import Viajes
from sqlalchemy.exc import SQLAlchemyError


def listar_viajes_por_viajante_service(id_usuario_viajante: str):
    """
    Obtiene la lista de viajes para un usuario viajante específico.
    """
    db = SessionLocal()
    try:
        usuario_existe = db.query(ViajeUsuario).filter(
            ViajeUsuario.id_usuario_viajante == id_usuario_viajante
        ).first()
        
        if not usuario_existe:
            return {
                "success": False,
                "detail": "El usuario viajante especificado no existe."
            }
        
        viajes_usuario = db.query(ViajeUsuario).filter(
            ViajeUsuario.id_usuario_viajante == id_usuario_viajante,
            ViajeUsuario.estado == True
        ).all()
        
        viajes_list = []
        for viaje_usuario in viajes_usuario:
            viaje = viaje_usuario.viaje
            
            if not viaje.estado:
                continue
            
            viajes_list.append({
                "id_viaje_usuario": viaje_usuario.id_viaje_usuario,
                "id_viaje": viaje.id_viaje,
                "nombre_viaje": viaje.nombre_viaje,
                "moneda_nombre": viaje.moneda.nombre,
                "estado_viaje": viaje.estado
            })
        
        if not viajes_list:
            return {
                "success": True,
                "detail": "No hay viajes disponibles para este usuario.",
                "data": []
            }
        
        return {
            "success": True,
            "detail": "Viajes obtenidos correctamente.",
            "data": viajes_list
        }
    except SQLAlchemyError as e:
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()
