from config.db import SessionLocal
from models.medios_pago import MediosPago
from sqlalchemy.exc import SQLAlchemyError


def deshabilitar_mediopago_service(id_medio_pago: int):
    """
    Deshabilita un medio de pago actualizando su estado a False.
    Solo es posible deshabilitar medios de pago que están habilitados (estado=True).
    """
    db = SessionLocal()
    try:
        medio_pago = db.query(MediosPago).filter(
            MediosPago.id_medio_pago == id_medio_pago
        ).first()
        
        if not medio_pago:
            raise Exception(f"Medio de pago con ID {id_medio_pago} no encontrado")
        
        if not medio_pago.estado:
            return {
                "success": False,
                "detail": "El medio de pago ya se encuentra deshabilitado."
            }
        
        medio_pago.estado = False
        
        db.commit()
        db.refresh(medio_pago)
        
        return {
            "success": True,
            "detail": f"El medio de pago '{medio_pago.nombre}' fue deshabilitado correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
