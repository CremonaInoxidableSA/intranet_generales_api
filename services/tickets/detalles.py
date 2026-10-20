from config.db import SessionLocal
from models.ticket_usuario import TicketUsuario
from models.viaje_usuario import ViajeUsuario


async def obtener_detalles_ticket_service(id_ticket: int, id_usuario_jwt: str, permisos_usuario: list):
    """
    Obtiene los detalles de un ticket específico.
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
        
        viaje_usuario = db.query(ViajeUsuario).filter(
            ViajeUsuario.id_viaje_usuario == ticket.id_viaje_usuario
        ).first()
        
        if not viaje_usuario:
            return {
                "success": False,
                "detail": "El viaje_usuario asociado no existe."
            }
        
        if not viaje_usuario.estado:
            return {
                "success": False,
                "detail": "El viaje_usuario no está activo."
            }
        
        if not viaje_usuario.viaje.estado:
            return {
                "success": False,
                "detail": "El viaje no está activo."
            }
        
        es_admin = "PERMISO_VER_TICKETS_ADMIN_RENDICIONES" in permisos_usuario
        es_propietario = viaje_usuario.id_usuario_viajante == id_usuario_jwt
        
        if not es_admin and not es_propietario:
            return {
                "success": False,
                "detail": "No tienes permiso para ver este ticket."
            }
        
        ticket_info = {
            "id_ticket": ticket.id_ticket,
            "nombre_imagen": ticket.nombre_imagen,
            "fecha_gasto": ticket.fecha_gasto,
            "monto": ticket.monto,
            "id_medio_pago": ticket.id_medio_pago,
            "id_moneda": ticket.id_moneda,
            "id_concepto": ticket.id_concepto,
            "estado_ticket_usuario": ticket.estado_ticket_usuario,
            "estado_ticket_admin": ticket.estado_ticket_admin,
        }
        
        if ticket.medio_pago:
            ticket_info["nombre_medio_pago"] = ticket.medio_pago.nombre_medio_pago
        else:
            ticket_info["nombre_medio_pago"] = None
        
        if ticket.moneda:
            ticket_info["nombre_moneda"] = ticket.moneda.nombre
        else:
            ticket_info["nombre_moneda"] = None
        
        if ticket.concepto:
            ticket_info["nombre_concepto"] = ticket.concepto.nombre_concepto
        else:
            ticket_info["nombre_concepto"] = None
        
        return {
            "success": True,
            "detail": "Detalles del ticket obtenidos correctamente.",
            "ticket": ticket_info
        }
    
    except Exception as e:
        return {
            "success": False,
            "detail": f"Error al obtener los detalles del ticket: {str(e)}"
        }
    
    finally:
        db.close()
