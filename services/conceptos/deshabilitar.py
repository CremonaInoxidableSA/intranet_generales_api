from config.db import SessionLocal
from models.conceptos import Conceptos
from sqlalchemy.exc import SQLAlchemyError


def deshabilitar_concepto_service(id_concepto: int):
    """
    Deshabilita un concepto actualizando su estado a False.
    Solo es posible deshabilitar conceptos que están habilitados (estado=True).
    """
    db = SessionLocal()
    try:
        concepto = db.query(Conceptos).filter(
            Conceptos.id_concepto == id_concepto
        ).first()
        
        if not concepto:
            raise Exception(f"Concepto con ID {id_concepto} no encontrado")
        
        if not concepto.estado:
            return {
                "success": False,
                "detail": "El concepto ya se encuentra deshabilitado."
            }
        
        concepto.estado = False
        
        db.commit()
        db.refresh(concepto)
        
        return {
            "success": True,
            "detail": f"El concepto '{concepto.nombre}' fue deshabilitado correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
