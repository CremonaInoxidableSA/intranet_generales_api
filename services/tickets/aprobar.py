from config.db import SessionLocal
from models.ticket_usuario import TicketUsuario
from sqlalchemy.exc import SQLAlchemyError


async def aprobar_ticket_service(
    id_ticket: int,
    id_usuario_jwt: str
):
    """
    Aprueba un ticket que se encuentre en estado "POR APROBAR".
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
        
        if ticket.estado == "APROBADO":
            return {
                "success": False,
                "detail": f"El ticket ya se encuentra aprobado"
            }
        
        if ticket.estado == "PENDIENTE":
            return {
                "success": False,
                "detail": f"El ticket se encuentra en estado 'PENDIENTE' porfavor, solicitar al viajante que complete sus datos para poder aprobarlo."
            }
        
        ticket.estado = "APROBADO"
        db.commit()
        
        return {
            "success": True,
            "detail": "Ticket aprobado exitosamente.",
            "ticket": {
                "id_ticket": ticket.id_ticket,
                "estado": ticket.estado
            }
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
            "detail": f"Error al aprobar el ticket: {str(e)}"
        }
    finally:
        db.close()
