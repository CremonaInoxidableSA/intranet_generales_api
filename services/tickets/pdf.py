import os
from config.db import SessionLocal
from models.ticket_usuario import TicketUsuario
from models.viaje_usuario import ViajeUsuario


async def validar_descarga_pdf(id_ticket: int, id_usuario: str, permisos_usuario: list) -> dict:
    """
    Valida si el usuario tiene permiso para descargar el PDF del ticket.
    Verifica que el archivo sea un PDF.
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
        
        es_pdf = False
        try:
            with open(ruta_completa, 'rb') as f:
                contenido_inicio = f.read(10)
                if b'%PDF' in contenido_inicio:
                    es_pdf = True
        except:
            pass
        
        extension = os.path.splitext(ruta_completa)[1].lower()
        if not es_pdf and extension == ".pdf":
            es_pdf = True
        
        if not es_pdf:
            return {
                "success": False,
                "detail": "El archivo no es un PDF válido"
            }
        
        if "PERMISO_VER_TICKETS_ADMIN_RENDICIONES" in permisos_usuario:
            return {
                "success": True,
                "ruta": ruta_completa,
                "nombre_archivo": filename
            }
        
        if "PERMISO_VER_TICKETS_RENDICIONES" in permisos_usuario:
            viaje_usuario = db.query(ViajeUsuario).filter(
                ViajeUsuario.id_viaje_usuario == ticket.id_viaje_usuario,
                ViajeUsuario.id_usuario_viajante == id_usuario
            ).first()
            
            if not viaje_usuario:
                return {
                    "success": False,
                    "detail": "No tienes permiso para descargar este PDF"
                }
            
            return {
                "success": True,
                "ruta": ruta_completa,
                "nombre_archivo": filename
            }
        
        return {
            "success": False,
            "detail": "No tienes permiso para descargar PDFs"
        }
    
    except Exception as e:
        return {
            "success": False,
            "detail": f"Error al validar descarga: {str(e)}"
        }
    
    finally:
        db.close()
