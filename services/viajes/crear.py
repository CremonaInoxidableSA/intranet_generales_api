from datetime import datetime
from config.db import SessionLocal
from models.viajes import Viajes
from models.monedas import Monedas
from sqlalchemy.exc import SQLAlchemyError


def crear_viaje_service(nombre_viaje: str, id_moneda: int):
    """
    Crea un nuevo viaje en la base de datos.
    Valida que el nombre_viaje no esté vacío y que la moneda exista y esté activa.
    """
    # Validar nombre_viaje
    if not nombre_viaje or not nombre_viaje.strip():
        return {
            "success": False,
            "detail": "El nombre del viaje no puede estar vacío."
        }
    
    db = SessionLocal()
    try:
        # Validar que id_moneda existe y está en estado true
        moneda = db.query(Monedas).filter(
            Monedas.id_moneda == id_moneda,
            Monedas.estado == True
        ).first()
        
        if not moneda:
            return {
                "success": False,
                "detail": "La moneda especificada no existe o no está activa."
            }
        
        # Validar que no existe otro viaje con el mismo nombre
        viaje_existente = db.query(Viajes).filter(
            Viajes.nombre_viaje == nombre_viaje.strip()
        ).first()
        
        if viaje_existente:
            return {
                "success": False,
                "detail": "Ya existe un viaje con ese nombre."
            }
        
        # Crear el nuevo viaje
        nuevo_viaje = Viajes(
            nombre_viaje=nombre_viaje.strip(),
            id_moneda=id_moneda,
            estado=True
        )
        
        db.add(nuevo_viaje)
        db.commit()
        db.refresh(nuevo_viaje)
        
        return {
            "success": True,
            "detail": f"Viaje '{nombre_viaje}' creado correctamente."
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()
