from config.db import SessionLocal
from models.medios_pago import MediosPago
from sqlalchemy.exc import SQLAlchemyError


def listar_mediospago_service():
    """
    Obtiene la lista de todos los medios de pago activos de la base de datos.
    """
    db = SessionLocal()
    try:
        medios_pago = db.query(MediosPago).all()
        
        if not medios_pago:
            return {
                "success": True,
                "detail": "No hay medios de pago disponibles.",
                "data": []
            }
        
        medios_pago_list = [
            {
                "id_medio_pago": medio_pago.id_medio_pago,
                "nombre": medio_pago.nombre,
                "estado": medio_pago.estado
            }
            for medio_pago in medios_pago
        ]
        
        return {
            "success": True,
            "detail": "Medios de pago obtenidos correctamente.",
            "data": medios_pago_list
        }
    except SQLAlchemyError as e:
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        db.close()
