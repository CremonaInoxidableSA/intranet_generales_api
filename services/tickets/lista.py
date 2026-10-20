from sqlalchemy import desc
from config.db import SessionLocal
from models.ticket_usuario import TicketUsuario
from models.viaje_usuario import ViajeUsuario
from models.monedas import Monedas
from models.conceptos import Conceptos
from models.medios_pago import MediosPago


async def listar_tickets_service(id_viaje_usuario: int):
    """
    Lista todos los tickets de un viaje_usuario específico.
    Devuelve los datos completos del ticket junto con la URL de la imagen.
    """
    db = SessionLocal()
    try:
        viaje_usuario = db.query(ViajeUsuario).filter(
            ViajeUsuario.id_viaje_usuario == id_viaje_usuario,
            ViajeUsuario.estado == True
        ).first()
        
        if not viaje_usuario:
            return {
                "success": False,
                "detail": "El viaje_usuario especificado no existe o no está activo."
            }
        
        tickets = db.query(TicketUsuario).filter(
            TicketUsuario.id_viaje_usuario == id_viaje_usuario
        ).order_by(desc(TicketUsuario.fecha_carga)).all()
        
        if not tickets:
            return {
                "success": True,
                "detail": "No hay tickets para este viaje.",
                "tickets": []
            }
        
        tickets_data = []
        for ticket in tickets:
            ticket_info = {
                "id_ticket": ticket.id_ticket,
                "nombre_imagen": ticket.nombre_imagen,
                "monto": ticket.monto,
                "id_moneda": ticket.id_moneda,
                "estado_ticket_usuario": ticket.estado_ticket_usuario
            }
            
            tickets_data.append(ticket_info)
        
        return {
            "success": True,
            "detail": f"Se encontraron {len(tickets_data)} ticket(s).",
            "tickets": tickets_data
        }
    
    except Exception as e:
        return {
            "success": False,
            "detail": f"Error al listar tickets: {str(e)}"
        }
    
    finally:
        db.close()
