import os
from datetime import date
from config.db import SessionLocal
from models.ticket_usuario import TicketUsuario
from models.viaje_usuario import ViajeUsuario
from models.medios_pago import MediosPago
from models.monedas import Monedas
from models.conceptos import Conceptos
from sqlalchemy.exc import SQLAlchemyError

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../../imagenes/tickets")


async def editar_ticket_service(
    id_ticket: int,
    nombre_imagen: str,
    monto: int,
    fecha_gasto: date,
    id_medio_pago: int,
    id_moneda: int,
    id_concepto: int,
    id_usuario_jwt: str
):
    """
    Edita un ticket existente.
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
                "detail": "No se pueden editar tickets aprobados."
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
        
        if viaje_usuario.id_usuario_viajante != id_usuario_jwt:
            return {
                "success": False,
                "detail": "No tienes permiso para editar este ticket."
            }
        
        medio_pago = db.query(MediosPago).filter(
            MediosPago.id_medio_pago == id_medio_pago
        ).first()
        
        if not medio_pago:
            return {
                "success": False,
                "detail": f"El medio de pago con ID {id_medio_pago} no existe."
            }
        
        if not medio_pago.estado:
            return {
                "success": False,
                "detail": f"El medio de pago con ID {id_medio_pago} no está activo."
            }
        
        moneda = db.query(Monedas).filter(
            Monedas.id_moneda == id_moneda
        ).first()
        
        if not moneda:
            return {
                "success": False,
                "detail": f"La moneda con ID {id_moneda} no existe."
            }
        
        if not moneda.estado:
            return {
                "success": False,
                "detail": f"La moneda con ID {id_moneda} no está activa."
            }
        
        concepto = db.query(Conceptos).filter(
            Conceptos.id_concepto == id_concepto
        ).first()
        
        if not concepto:
            return {
                "success": False,
                "detail": f"El concepto con ID {id_concepto} no existe."
            }
        
        if not concepto.estado:
            return {
                "success": False,
                "detail": f"El concepto con ID {id_concepto} no está activo."
            }
        
        if nombre_imagen != ticket.nombre_imagen:
            if ".." in nombre_imagen or "/" in nombre_imagen or "\\" in nombre_imagen:
                return {
                    "success": False,
                    "detail": "Nombre de archivo inválido."
                }
            
            nombre_sin_ext, ext_antigua = os.path.splitext(ticket.nombre_imagen)
            nombre_nuevo_sin_ext, ext_nueva = os.path.splitext(nombre_imagen)
            
            if not ext_nueva:
                nombre_imagen = nombre_nuevo_sin_ext + ext_antigua
            else:
                nombre_imagen = nombre_nuevo_sin_ext + ext_antigua
            
            ruta_antigua = os.path.join(UPLOAD_DIR, ticket.nombre_imagen)
            ruta_nueva = os.path.join(UPLOAD_DIR, nombre_imagen)
            
            if not os.path.exists(ruta_antigua):
                return {
                    "success": False,
                    "detail": "El archivo actual no existe en el servidor."
                }
            
            if os.path.exists(ruta_nueva):
                return {
                    "success": False,
                    "detail": "El nuevo nombre de archivo ya existe."
                }
            
            try:
                os.rename(ruta_antigua, ruta_nueva)
            except Exception as e:
                return {
                    "success": False,
                    "detail": f"Error al renombrar el archivo: {str(e)}"
                }
        
        ticket.nombre_imagen = nombre_imagen
        ticket.monto = monto
        ticket.fecha_gasto = fecha_gasto
        ticket.id_medio_pago = id_medio_pago
        ticket.id_moneda = id_moneda
        ticket.id_concepto = id_concepto
        ticket.estado = "POR APROBAR"
        
        db.commit()
        
        return {
            "success": True,
            "detail": "Ticket actualizado exitosamente.",
            "ticket": {
                "id_ticket": ticket.id_ticket,
                "nombre_imagen": ticket.nombre_imagen,
                "monto": ticket.monto,
                "fecha_gasto": ticket.fecha_gasto,
                "id_medio_pago": ticket.id_medio_pago,
                "id_moneda": ticket.id_moneda,
                "id_concepto": ticket.id_concepto,
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
            "detail": f"Error al editar el ticket: {str(e)}"
        }
    finally:
        db.close()
