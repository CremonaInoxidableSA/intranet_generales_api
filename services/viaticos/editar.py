from config.db import SessionLocal
from models.viaticos import Viaticos
from models.monedas import Monedas
from sqlalchemy.exc import SQLAlchemyError


def editar_viaticos_service(
    id_viatico: int,
    id_usuario_viajante: str,
    id_moneda: int,
    monto_entregado: int,
    monto_devuelto: int | None
):
    """
    Edita un viatico existente.
    Valida que:
    - El viatico existe
    - El id_moneda existe y está activo
    - Solo el usuario propietario del viatico puede editarlo
    - El viaje_usuario associated está activo (estado = True)
    """
    
    db = SessionLocal()
    try:
        viatico = db.query(Viaticos).filter(
            Viaticos.id_viatico == id_viatico
        ).first()
        
        if not viatico:
            return {
                "success": False,
                "detail": "El viatico especificado no existe."
            }
        
        if viatico.estado == True:
            return {
                "success": False,
                "detail": "El viatico ya está aprobado y no puede modificarse."
            }
        
        viaje_usuario = viatico.viaje_usuario
        
        if viaje_usuario.id_usuario_viajante != id_usuario_viajante:
            return {
                "success": False,
                "detail": "Solo puede editar viaticos propios."
            }
        
        if not viaje_usuario.estado:
            return {
                "success": False,
                "detail": "El viaje para este usuario no está activo."
            }
        
        moneda = db.query(Monedas).filter(
            Monedas.id_moneda == id_moneda,
            Monedas.estado == True
        ).first()
        
        if not moneda:
            return {
                "success": False,
                "detail": "La moneda especificada no existe o no está activa."
            }
        
        viatico.id_moneda = id_moneda
        viatico.monto_entregado = monto_entregado
        viatico.monto_devuelto = monto_devuelto
        
        db.commit()
        db.refresh(viatico)
        
        return {
            "success": True,
            "detail": "Viatico actualizado correctamente.",
            "id_viatico": viatico.id_viatico
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()
