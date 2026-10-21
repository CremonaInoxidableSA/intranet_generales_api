import os
from config.db import SessionLocal
from models.ticket_usuario import TicketUsuario
from sqlalchemy.exc import SQLAlchemyError

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../../imagenes/tickets")


async def eliminar_ticket_service(
    id_ticket: int,
    id_usuario_jwt: str
):
    """
    Elimina un ticket y su imagen asociada.
    """
    db = SessionLocal()
    try:
        ticket = db.query(TicketUsuario).filter(
            TicketUsuario.id_ticket == id_ticket
        ).first()
        
        if not ticket:
            return {
                "success": False,
                "detail": "El ticket no existe."
            }
        
        ruta_imagen = os.path.join(UPLOAD_DIR, ticket.nombre_imagen)
        
        if os.path.exists(ruta_imagen):
            try:
                os.remove(ruta_imagen)
            except Exception as e:
                return {
                    "success": False,
                    "detail": f"Error al eliminar la imagen: {str(e)}"
                }
        
        db.delete(ticket)
        db.commit()
        
        return {
            "success": True,
            "detail": "Ticket eliminado exitosamente."
        }
    
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "detail": f"Error al eliminar el ticket: {str(e)}"
        }
    finally:
        db.close()
