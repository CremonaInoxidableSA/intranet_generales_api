from sqlalchemy import desc
from config.db import SessionLocal
from models.ticket_usuario import TicketUsuario
from models.viaje_usuario import ViajeUsuario


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
                "url_imagen": f"http://localhost:8205/imagenes/tickets/{ticket.nombre_imagen}",
                "fecha_carga": ticket.fecha_carga,
                "fecha_gasto": ticket.fecha_gasto,
                "monto": ticket.monto,
                "estado_ticket_usuario": ticket.estado_ticket_usuario,
                "estado_ticket_admin": ticket.estado_ticket_admin,
            }
            
            if ticket.medio_pago:
                ticket_info["medio_pago"] = {
                    "id": ticket.medio_pago.id_medio_pago,
                    "nombre": ticket.medio_pago.nombre_medio_pago
                }
            
            if ticket.moneda:
                ticket_info["moneda"] = {
                    "id": ticket.moneda.id_moneda,
                    "nombre": ticket.moneda.nombre_moneda,
                    "simbolo": ticket.moneda.simbolo
                }
            
            if ticket.concepto:
                ticket_info["concepto"] = {
                    "id": ticket.concepto.id_concepto,
                    "nombre": ticket.concepto.nombre_concepto
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
