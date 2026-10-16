from config.db import SessionLocal
from models.monedas import Monedas
from sqlalchemy.exc import SQLAlchemyError


def listar_monedas_service():
    """
    Obtiene la lista de todas las monedas activas de la base de datos.
    """
    db = SessionLocal()
    try:
        monedas = db.query(Monedas).all()
        
        if not monedas:
            return {
                "success": True,
                "detail": "No hay monedas disponibles.",
                "data": []
            }
        
        monedas_list = [
            {
                "id_moneda": moneda.id_moneda,
                "nombre": moneda.nombre,
                "estado": moneda.estado
            }
            for moneda in monedas
        ]
        
        return {
            "success": True,
            "detail": "Monedas obtenidas correctamente.",
            "data": monedas_list
        }
    except SQLAlchemyError as e:
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
