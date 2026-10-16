from config.db import SessionLocal
from models.conceptos import Conceptos
from sqlalchemy.exc import SQLAlchemyError


def habilitar_concepto_service(id_concepto: int):
    """
    Habilita un concepto actualizando su estado a True.
    Solo es posible habilitar conceptos que están deshabilitados (estado=False).
    """
    db = SessionLocal()
    try:
        concepto = db.query(Conceptos).filter(
            Conceptos.id_concepto == id_concepto
        ).first()
        
        if not concepto:
            raise Exception(f"Concepto con ID {id_concepto} no encontrado")
        
        if concepto.estado:
            return {
                "success": False,
                "detail": "El concepto ya se encuentra habilitado."
            }
        
        concepto.estado = True
        
        db.commit()
        db.refresh(concepto)
        
        return {
            "success": True,
            "detail": f"El concepto '{concepto.nombre}' fue habilitado correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
