from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

from config import db
from config.sql_loader import cargar_datos_iniciales

from models.comentarios import Comentarios
from models.conceptos import Conceptos
from models.medios_pago import MediosPago
from models.monedas import Monedas
from models.ticket_usuario import TicketUsuario
from models.viaje_usuario import ViajeUsuario
from models.viajes import Viajes
from models.viaticos import Viaticos

from routers.viajes.lista import router as viajes_lista_router
from routers.viajes.crear import router as viajes_crear_router
from routers.viajes.habilitar import router as viajes_habilitar_router
from routers.viajes.deshabilitar import router as viajes_deshabilitar_router
from routers.viajes.editarviajantes import router as viajes_editarviajantes_router
from routers.viajes.editarmoneda import router as viajes_editarmoneda_router
from routers.viajes.detalles import router as viajes_detalles_router
from routers.viajes.listaviajante import router as viajes_listaviajante_router

from routers.monedas.lista import router as monedas_lista_router
from routers.monedas.crear import router as monedas_crear_router
from routers.monedas.habilitar import router as monedas_habilitar_router
from routers.monedas.deshabilitar import router as monedas_deshabilitar_router

from routers.medios_pago.lista import router as mediopago_lista_router
from routers.medios_pago.crear import router as mediopago_crear_router
from routers.medios_pago.habilitar import router as mediopago_habilitar_router
from routers.medios_pago.deshabilitar import router as mediopago_deshabilitar_router

from routers.conceptos.lista import router as conceptos_lista_router
from routers.conceptos.crear import router as conceptos_crear_router
from routers.conceptos.habilitar import router as conceptos_habilitar_router
from routers.conceptos.deshabilitar import router as conceptos_deshabilitar_router

from routers.comentarios.crear import router as comentarios_crear_router
from routers.comentarios.listaviaje import router as comentarios_listaviaje_router

from routers.viaticos.crear import router as viaticos_crear_router
from routers.viaticos.editar import router as viaticos_editar_router
from routers.viaticos.aprobar import router as viaticos_aprobar_router
from routers.viaticos.listaviaje import router as viaticos_listaviaje_router

from routers.tickets.cargar import router as tickets_cargar_router
from routers.tickets.lista import router as tickets_lista_router
from routers.tickets.imagen import router as tickets_imagen_router
from routers.tickets.detalles import router as tickets_detalles_router

load_dotenv()
    
with create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{quote_plus(os.getenv('DB_PASSWORD', ''))}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
).connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}"))
    print(f"✓ Base de datos '{os.getenv('DB_NAME')}' verificada o creada exitosamente")

#db.Base.metadata.drop_all(bind=db.engine)
#db.Base.metadata.create_all(bind=db.engine)
cargar_datos_iniciales()

app = FastAPI(title="API cr_generales", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(viajes_lista_router)
app.include_router(viajes_listaviajante_router)
app.include_router(viajes_detalles_router)
app.include_router(viajes_crear_router)
app.include_router(viajes_habilitar_router)
app.include_router(viajes_deshabilitar_router)
app.include_router(viajes_editarviajantes_router)
app.include_router(viajes_editarmoneda_router)

app.include_router(monedas_lista_router)
app.include_router(monedas_crear_router)
app.include_router(monedas_habilitar_router)
app.include_router(monedas_deshabilitar_router)

app.include_router(mediopago_lista_router)
app.include_router(mediopago_crear_router)
app.include_router(mediopago_habilitar_router)
app.include_router(mediopago_deshabilitar_router)

app.include_router(conceptos_lista_router)
app.include_router(conceptos_crear_router)
app.include_router(conceptos_habilitar_router)
app.include_router(conceptos_deshabilitar_router)

app.include_router(comentarios_crear_router)
app.include_router(comentarios_listaviaje_router)

app.include_router(viaticos_crear_router)
app.include_router(viaticos_editar_router)
app.include_router(viaticos_aprobar_router)
app.include_router(viaticos_listaviaje_router)

app.include_router(tickets_cargar_router)
app.include_router(tickets_lista_router)
app.include_router(tickets_imagen_router)
app.include_router(tickets_detalles_router)