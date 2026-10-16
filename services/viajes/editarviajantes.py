from config.db import SessionLocal
from models.viajes import Viajes
from models.viaje_usuario import ViajeUsuario
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any


def editar_viajantes_service(id_viaje: int, viajantes: List[Dict[str, Any]]):
    """
    Actualiza el estado de los viajantes para un viaje.
    - Los viajantes en la lista se marcan con estado = True
    - Los viajantes fuera de la lista se marcan con estado = False
    - No elimina registros, solo actualiza el estado
    """
    db = SessionLocal()
    try:
        # Validar que el viaje existe y está en estado true
        viaje = db.query(Viajes).filter(
            Viajes.id_viaje == id_viaje,
            Viajes.estado == True
        ).first()
        
        if not viaje:
            return {
                "success": False,
                "detail": "El viaje especificado no existe o no está activo."
            }
        
        # Extraer los ids de los viajantes que están en la nueva lista
        ids_nuevos_viajantes = set()
        viajantes_a_actualizar = []
        
        for viajante in viajantes:
            id_usuario = viajante.id_usuario_viajante
            ids_nuevos_viajantes.add(id_usuario)
            
            nombre_usuario = viajante.nombre_usuario_viajante
            apellido_usuario = viajante.apellido_usuario_viajante
            legajo_usuario = viajante.legajo_usuario_viajante
            
            # Buscar si el viajante ya existe
            usuario_existente = db.query(ViajeUsuario).filter(
                ViajeUsuario.id_viaje == id_viaje,
                ViajeUsuario.id_usuario_viajante == id_usuario
            ).first()
            
            if usuario_existente:
                # Si existe, actualizar su estado a True y sus datos
                usuario_existente.estado = True
                usuario_existente.nombre_usuario_viajante = nombre_usuario
                usuario_existente.apellido_usuario_viajante = apellido_usuario
                usuario_existente.legajo_usuario_viajante = legajo_usuario
            else:
                # Si no existe, crear uno nuevo con estado True
                nuevo_viajante = ViajeUsuario(
                    id_viaje=id_viaje,
                    id_usuario_viajante=id_usuario,
                    nombre_usuario_viajante=nombre_usuario,
                    apellido_usuario_viajante=apellido_usuario,
                    legajo_usuario_viajante=legajo_usuario,
                    estado=True
                )
                db.add(nuevo_viajante)
        
        # Obtener todos los viajantes del viaje
        todos_viajantes = db.query(ViajeUsuario).filter(
            ViajeUsuario.id_viaje == id_viaje
        ).all()
        
        # Marcar como estado = False los que no están en la nueva lista
        for viajante in todos_viajantes:
            if viajante.id_usuario_viajante not in ids_nuevos_viajantes:
                viajante.estado = False
        
        db.commit()
        
        response = {
            "success": True,
            "detail": "Los viajantes se han actualizado correctamente."
        }
        
        return response
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()
