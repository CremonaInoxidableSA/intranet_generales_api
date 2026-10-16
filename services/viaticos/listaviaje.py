from config.db import SessionLocal
from models.viaticos import Viaticos
from models.monedas import Monedas
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc


def listar_viaticos_por_viaje_service(id_viaje_usuario: int):
    """
    Obtiene la lista de viáticos de un viaje_usuario específico.
    """
    db = SessionLocal()
    try:
        viaticos = db.query(Viaticos).filter(
            Viaticos.id_viaje_usuario == id_viaje_usuario).all()
        
        if not viaticos:
            return {
                "success": True,
                "detail": "No hay viáticos disponibles para este viaje.",
                "data": []
            }
        
        viaticos_list = [
            {
                "id_viatico": viatico.id_viatico,
                "moneda": viatico.moneda.nombre,
                "monto_entregado": viatico.monto_entregado,
                "monto_devuelto": viatico.monto_devuelto,
                "estado": viatico.estado
            }
            for viatico in viaticos
        ]
        
        return {
            "success": True,
            "detail": "Viáticos obtenidos correctamente.",
            "data": viaticos_list
        }
    except SQLAlchemyError as e:
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()
