import os
from datetime import datetime
from fastapi import UploadFile
from config.db import SessionLocal
from models.viaje_usuario import ViajeUsuario
from models.ticket_usuario import TicketUsuario
from sqlalchemy.exc import SQLAlchemyError

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../../imagenes/tickets")

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}


def obtener_nombre_unico(nombre_original: str) -> str:
    """
    Si el archivo ya existe, agrega un número entre paréntesis.
    """
    if not os.path.exists(os.path.join(UPLOAD_DIR, nombre_original)):
        return nombre_original
    
    nombre_base, extension = os.path.splitext(nombre_original)
    contador = 1
    
    while os.path.exists(os.path.join(UPLOAD_DIR, f"{nombre_base}({contador}){extension}")):
        contador += 1
    
    return f"{nombre_base}({contador}){extension}"


async def cargar_tickets_service(id_viaje_usuario: int, archivos: list[UploadFile], id_usuario_jwt: str):
    """
    Crea registros en ticket_usuario con validaciones de propiedad y estado.
    """
    db = SessionLocal()
    try:
        if len(archivos) > 30:
            return {
                "success": False,
                "detail": "No se pueden cargar más de 30 imágenes a la vez."
            }
        
        if len(archivos) < 1:
            return {
                "success": False,
                "detail": "Debe cargar al menos una imagen."
            }
        
        viaje_usuario = db.query(ViajeUsuario).filter(
            ViajeUsuario.id_viaje_usuario == id_viaje_usuario
        ).first()
        
        if not viaje_usuario:
            return {
                "success": False,
                "detail": "El viaje_usuario especificado no existe."
            }
        
        if not viaje_usuario.estado:
            return {
                "success": False,
                "detail": "El viaje_usuario no está activo."
            }
        
        if viaje_usuario.id_usuario_viajante != id_usuario_jwt:
            return {
                "success": False,
                "detail": "No tienes permiso para cargar tickets en este viaje."
            }
        
        if not viaje_usuario.viaje.estado:
            return {
                "success": False,
                "detail": "El viaje asociado no está activo."
            }
        
        tickets_creados = []
        errores = []
        
        for archivo in archivos:
            extension = os.path.splitext(archivo.filename)[1].lower()
            if extension not in ALLOWED_EXTENSIONS:
                errores.append(f"El archivo '{archivo.filename}' no se cargó, recorda que solo se aceptan archivos de formato PNG, JPEG, JPG, PDF")
                continue
            
            try:
                nombre_unico = obtener_nombre_unico(archivo.filename)
                ruta_archivo = os.path.join(UPLOAD_DIR, nombre_unico)
                
                contenido = await archivo.read()
                with open(ruta_archivo, "wb") as f:
                    f.write(contenido)
                
                ticket = TicketUsuario(
                    id_viaje_usuario=id_viaje_usuario,
                    fecha_carga=datetime.now(),
                    nombre_imagen=nombre_unico,
                    estado="PENDIENTE",
                    id_moneda=viaje_usuario.viaje.id_moneda
                )
                
                db.add(ticket)
                tickets_creados.append(nombre_unico)
                
            except Exception as e:
                errores.append(f"{archivo.filename}: Error al procesar - {str(e)}")
                continue
        
        if tickets_creados:
            db.commit()
        
        respuesta = {
            "success": True,
            "detail": f"Se cargaron {len(tickets_creados)} ticket(s) correctamente.",
        }
        
        if errores:
            respuesta["errores"] = errores
        
        return respuesta
        
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "success": False,
            "detail": f"Error en la base de datos: {str(e)}"
        }
    finally:
        db.close()