import pandas as pd
from io import BytesIO
from sqlalchemy import desc
from config.db import SessionLocal
from models.ticket_usuario import TicketUsuario
from models.viaje_usuario import ViajeUsuario
from models.viaticos import Viaticos
from models.monedas import Monedas
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


async def generar_excel_tickets_service(id_viaje_usuario: int):
    """
    Genera un archivo Excel con resumen de gastos en una sola hoja.
    """
    db = SessionLocal()
    try:
        viaje_usuario = db.query(ViajeUsuario).filter(
            ViajeUsuario.id_viaje_usuario == id_viaje_usuario,
            ViajeUsuario.estado == True
        ).first()
        
        if not viaje_usuario:
            return {
                "success": False,
                "detail": "El viaje_usuario especificado no existe o no está activo."
            }
        
        # Obtener todas las monedas
        monedas = db.query(Monedas).all()
        monedas_dict = {m.id_moneda: m.nombre for m in monedas}
        
        # Crear workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte"
        
        # Estilos
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        row = 1
        
        # TABLA 1: Resumen de gastos por moneda
        ws[f'A{row}'] = "RESUMEN DE GASTOS"
        ws[f'A{row}'].font = Font(bold=True, size=12)
        row += 2
        
        # Headers de la tabla 1
        headers_tabla1 = ["Moneda", "Efectivo Entregado", "Efectivo Devuelto", "Total de Gastos Rendidos", "Diferencia"]
        for col, header in enumerate(headers_tabla1, 1):
            cell = ws.cell(row=row, column=col)
            cell.value = header
            cell.fill = header_fill
            cell.font = header_font
            cell.border = border
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        row += 1
        
        # Datos tabla 1
        for moneda in monedas:
            # Obtener viaticos no pendientes (estado = True) para esta moneda
            viaticos = db.query(Viaticos).filter(
                Viaticos.id_viaje_usuario == id_viaje_usuario,
                Viaticos.id_moneda == moneda.id_moneda,
                Viaticos.estado == True
            ).all()
            
            efectivo_entregado = sum(v.monto_entregado or 0 for v in viaticos)
            efectivo_devuelto = sum(v.monto_devuelto or 0 for v in viaticos)
            
            # Obtener tickets de efectivo (id_medio_pago = 1) para esta moneda
            tickets_efectivo = db.query(TicketUsuario).filter(
                TicketUsuario.id_viaje_usuario == id_viaje_usuario,
                TicketUsuario.id_moneda == moneda.id_moneda,
                TicketUsuario.id_medio_pago == 1
            ).all()
            
            total_gastos_rendidos = sum(t.monto or 0 for t in tickets_efectivo)
            
            # Calcular diferencia
            diferencia = efectivo_entregado - efectivo_devuelto - total_gastos_rendidos
            
            # Escribir datos
            ws.cell(row=row, column=1).value = moneda.nombre
            ws.cell(row=row, column=2).value = efectivo_entregado
            ws.cell(row=row, column=3).value = efectivo_devuelto
            ws.cell(row=row, column=4).value = total_gastos_rendidos
            ws.cell(row=row, column=5).value = diferencia
            
            for col in range(1, 6):
                ws.cell(row=row, column=col).border = border
            
            row += 1
        
        row += 2
        
        # TABLA 2: Tickets de efectivo (id_medio_pago = 1)
        ws[f'A{row}'] = "TICKETS DE EFECTIVO"
        ws[f'A{row}'].font = Font(bold=True, size=12)
        row += 2
        
        tickets_efectivo_all = db.query(TicketUsuario).filter(
            TicketUsuario.id_viaje_usuario == id_viaje_usuario,
            TicketUsuario.id_medio_pago == 1
        ).order_by(desc(TicketUsuario.fecha_carga)).all()
        
        if tickets_efectivo_all:
            # Headers tabla 2
            headers_tabla2 = ["ID Ticket", "Fecha Carga", "Fecha Gasto", "Nombre Imagen", "Monto", "Moneda", "Concepto", "Estado"]
            for col, header in enumerate(headers_tabla2, 1):
                cell = ws.cell(row=row, column=col)
                cell.value = header
                cell.fill = header_fill
                cell.font = header_font
                cell.border = border
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            row += 1
            
            # Datos tabla 2
            for ticket in tickets_efectivo_all:
                ws.cell(row=row, column=1).value = ticket.id_ticket
                ws.cell(row=row, column=2).value = ticket.fecha_carga
                ws.cell(row=row, column=3).value = ticket.fecha_gasto
                ws.cell(row=row, column=4).value = ticket.nombre_imagen
                ws.cell(row=row, column=5).value = ticket.monto
                ws.cell(row=row, column=6).value = monedas_dict.get(ticket.id_moneda, "")
                ws.cell(row=row, column=7).value = ticket.id_concepto
                ws.cell(row=row, column=8).value = ticket.estado
                
                for col in range(1, 9):
                    ws.cell(row=row, column=col).border = border
                
                row += 1
        
        row += 2
        
        # TABLA 3: Tickets de otros medios de pago (id_medio_pago != 1)
        ws[f'A{row}'] = "TICKETS DE OTROS MEDIOS DE PAGO"
        ws[f'A{row}'].font = Font(bold=True, size=12)
        row += 2
        
        tickets_otros = db.query(TicketUsuario).filter(
            TicketUsuario.id_viaje_usuario == id_viaje_usuario,
            TicketUsuario.id_medio_pago != 1
        ).order_by(desc(TicketUsuario.fecha_carga)).all()
        
        if tickets_otros:
            # Headers tabla 3
            headers_tabla3 = ["ID Ticket", "Fecha Carga", "Fecha Gasto", "Nombre Imagen", "Monto", "Moneda", "Medio Pago", "Concepto", "Estado"]
            for col, header in enumerate(headers_tabla3, 1):
                cell = ws.cell(row=row, column=col)
                cell.value = header
                cell.fill = header_fill
                cell.font = header_font
                cell.border = border
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            row += 1
            
            # Datos tabla 3
            for ticket in tickets_otros:
                ws.cell(row=row, column=1).value = ticket.id_ticket
                ws.cell(row=row, column=2).value = ticket.fecha_carga
                ws.cell(row=row, column=3).value = ticket.fecha_gasto
                ws.cell(row=row, column=4).value = ticket.nombre_imagen
                ws.cell(row=row, column=5).value = ticket.monto
                ws.cell(row=row, column=6).value = monedas_dict.get(ticket.id_moneda, "")
                ws.cell(row=row, column=7).value = ticket.id_medio_pago
                ws.cell(row=row, column=8).value = ticket.id_concepto
                ws.cell(row=row, column=9).value = ticket.estado
                
                for col in range(1, 10):
                    ws.cell(row=row, column=col).border = border
                
                row += 1
        
        # Ajustar ancho de columnas
        ws.column_dimensions['A'].width = 15
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 20
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 12
        ws.column_dimensions['G'].width = 12
        ws.column_dimensions['H'].width = 12
        ws.column_dimensions['I'].width = 12
        
        # Guardar en BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return {
            "success": True,
            "file": output
        }
    
    except Exception as e:
        return {
            "success": False,
            "detail": f"Error al generar Excel: {str(e)}"
        }
    
    finally:
        db.close()
