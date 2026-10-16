from config.db import SessionLocal
from models.viaticos import Viaticos
from sqlalchemy.exc import SQLAlchemyError


def aprobar_viaticos_service(id_viatico: int):
    """
    Aprueba un viatico cambiando su estado a True.
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
        
        if viatico.estado:
            return {
                "success": False,
                "detail": "El viatico ya se encuentra aprobado."
            }
        
        viatico.estado = True
        db.commit()
        db.refresh(viatico)
        
        return {
            "success": True,
            "detail": "Viatico aprobado correctamente.",
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
