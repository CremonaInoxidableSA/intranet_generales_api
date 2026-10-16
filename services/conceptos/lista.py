from config.db import SessionLocal
from models.conceptos import Conceptos
from sqlalchemy.exc import SQLAlchemyError


def listar_conceptos_service():
    """
    Obtiene la lista de todos los conceptos activos de la base de datos.
    """
    db = SessionLocal()
    try:
        conceptos = db.query(Conceptos).all()
        
        if not conceptos:
            return {
                "success": True,
                "detail": "No hay conceptos disponibles.",
                "data": []
            }
        
        conceptos_list = [
            {
                "id_concepto": concepto.id_concepto,
                "nombre": concepto.nombre,
                "estado": concepto.estado
            }
            for concepto in conceptos
        ]
        
        return {
            "success": True,
            "detail": "Conceptos obtenidos correctamente.",
            "data": conceptos_list
        }
    except SQLAlchemyError as e:
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
