from tkinter import filedialog, messagebox
import tkinter as tk
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_payment_receipt(pago_id, alumno_seleccionado, materia, monto, divisa, metodo, cuota, correspondencia):
    """
    Genera un recibo de pago en PDF y permite al usuario elegir dónde guardarlo.
    
    Args:
        pago_id: ID del pago en la base de datos
        alumno_data: Diccionario con datos del alumno (nombre, apellido, dni)
        pago_data: Diccionario con los datos del pago (monto, divisa, etc.)
    
    Returns:
        str: Ruta del archivo PDF generado o None si hubo error
    """
    try:
        # Solicitar al usuario la ubicación para guardar el archivo
        
        archivo_destino = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"recibo_pago_{pago_id}.pdf",
            title="Guardar recibo de pago",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not archivo_destino:
            return None
            
        # Crear el documento PDF
        doc = SimpleDocTemplate(
            archivo_destino,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=16,
            spaceAfter=30
        )
        
        # Contenido del documento
        elementos = []

        # Dic para divisas
        simbolo_divisa = {
            "Peso": "ARS$",
            "Real": "R$",
            "Dolar": "USD$"
        }
        
        # Título
        elementos.append(Paragraph("RECIBO DE PAGO", titulo_style))
        elementos.append(Spacer(1, 20))
        
        # Información del recibo
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        info_recibo = [
            ["Número de Recibo:", str(pago_id)],
            ["Fecha:", fecha_actual],
            ["", ""],
            ["DATOS DEL ALUMNO", ""],
            ["Nombre y Apellido:", alumno_seleccionado.split(" - ")[1]],
            ["", ""],
            ["DATOS DEL PAGO", ""],
            ["Monto:", f"{monto} {simbolo_divisa[divisa]}"],
            ["Método de Pago:", f"{metodo}"],
            ["Cuota:", f"{cuota}"],
            ["Cuenta:", f"{correspondencia}"],
            ["Materia:", f"{materia}"]
        ]
        
        # Crear tabla con la información
        tabla = Table(info_recibo, colWidths=[4*inch, 3*inch])
        tabla.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, 0), 1, colors.black),
            ('BACKGROUND', (0, 3), (-1, 3), colors.lightgrey),
            ('BACKGROUND', (0, 7), (-1, 7), colors.lightgrey),
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 40))
        
        # Pie del recibo
        elementos.append(Paragraph("Este recibo es un comprobante válido de pago.", styles['Normal']))
        
        # Generar el PDF
        doc.build(elementos)
        
        return archivo_destino
        
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al generar el recibo: {str(e)}"
        )
        return None

