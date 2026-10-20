import os
from config.db import SessionLocal
from models.ticket_usuario import TicketUsuario
from models.viaje_usuario import ViajeUsuario


async def validar_acceso_imagen(id_ticket: int, id_usuario: str, permisos_usuario: list) -> dict:
    """
    Valida si el usuario tiene permiso para acceder a la imagen del ticket.
    """
    db = SessionLocal()
    try:
        ticket = db.query(TicketUsuario).filter(
            TicketUsuario.id_ticket == id_ticket
        ).first()
        
        if not ticket:
            return {
                "success": False,
                "detail": "El ticket no existe"
            }
        
        filename = ticket.nombre_imagen
        
        if ".." in filename or "/" in filename or "\\" in filename:
            return {
                "success": False,
                "detail": "Nombre de archivo inválido"
            }
        
        UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../../imagenes/tickets")
        ruta_completa = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.abspath(ruta_completa).startswith(os.path.abspath(UPLOAD_DIR)):
            return {
                "success": False,
                "detail": "Acceso denegado"
            }
        
        if not os.path.exists(ruta_completa):
            return {
                "success": False,
                "detail": "Archivo no encontrado"
            }
        
        if "PERMISO_VER_TICKETS_ADMIN_RENDICIONES" in permisos_usuario:
            return {
                "success": True,
                "ruta": ruta_completa
            }
        
        if "PERMISO_VER_TICKETS_RENDICIONES" in permisos_usuario:
            viaje_usuario = db.query(ViajeUsuario).filter(
                ViajeUsuario.id_viaje_usuario == ticket.id_viaje_usuario,
                ViajeUsuario.id_usuario_viajante == id_usuario
            ).first()
            
            if not viaje_usuario:
                return {
                    "success": False,
                    "detail": "No tienes permiso para ver esta imagen"
                }
            
            return {
                "success": True,
                "ruta": ruta_completa
            }
        
        return {
            "success": False,
            "detail": "No tienes permiso para ver imágenes"
        }
    
    except Exception as e:
        return {
            "success": False,
            "detail": f"Error al validar acceso: {str(e)}"
        }
    
    finally:
        db.close()
