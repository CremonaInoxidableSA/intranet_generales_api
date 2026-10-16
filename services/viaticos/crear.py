from config.db import SessionLocal
from models.viaje_usuario import ViajeUsuario
from models.viaticos import Viaticos
from models.monedas import Monedas
from sqlalchemy.exc import SQLAlchemyError


def crear_viaticos_service(
    id_viaje_usuario: int,
    id_usuario_viajante: str,
    id_moneda: int,
    monto_entregado: int,
    monto_devuelto: int | None
):
    """
    Crea un nuevo viatico en la base de datos.
    """
    
    db = SessionLocal()
    try:
        viaje_usuario = db.query(ViajeUsuario).filter(
            ViajeUsuario.id_viaje_usuario == id_viaje_usuario
        ).first()
        
        if not viaje_usuario:
            return {
                "success": False,
                "detail": "El viaje al cual está queriendo agregar el viatico no existe."
            }

        if viaje_usuario.estado == False:
            return {
                "success": False,
                "detail": "El viaje para este usuario no está activo."
            }

        if viaje_usuario.id_usuario_viajante != id_usuario_viajante:
            return {
                "success": False,
                "detail": "Solo puede cargar viaticos al viaje el usuario viajante."
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
        
        nuevo_viatico = Viaticos(
            id_viaje_usuario=id_viaje_usuario,
            id_moneda=id_moneda,
            monto_entregado=monto_entregado,
            monto_devuelto=monto_devuelto
        )
        
        db.add(nuevo_viatico)
        db.commit()
        db.refresh(nuevo_viatico)
        
        return {
            "success": True,
            "detail": "Viatico creado correctamente.",
            "id_viatico": nuevo_viatico.id_viatico
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()
