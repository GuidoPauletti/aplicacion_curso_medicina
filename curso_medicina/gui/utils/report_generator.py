# gui/utils/pdf_generator.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self, tree_data):
        """
        Inicializa el generador de PDF con los datos del TreeView
        """
        self.tree_data = tree_data
        self.styles = getSampleStyleSheet()
        
    def _get_table_data(self):
        """
        Obtiene y organiza los datos de la tabla, separando entradas y salidas
        """
        entradas = []
        salidas = []
        total_entradas = 0
        total_salidas = 0
        
        # Procesar cada fila
        for item in self.tree_data:
            row = list(item)  # Convertir la tupla en lista
            if row[1] == "Entrada":  # El índice 1 corresponde al Tipo
                entradas.append(row)
                total_entradas += float(row[2])  # El índice 2 corresponde al Monto
            else:
                salidas.append(row)
                total_salidas += float(row[2])
                
        return {
            'entradas': entradas,
            'salidas': salidas,
            'total_entradas': total_entradas,
            'total_salidas': total_salidas,
            'balance': total_entradas - total_salidas
        }
    
    def generate_pdf(self, output_path):
        """
        Genera el PDF con el informe financiero
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Preparar los elementos del documento
        elements = []
        
        # Añadir fecha
        date_style = ParagraphStyle(
            'CustomDateStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=30
        )
        current_date = datetime.now().strftime("%d/%m/%Y")
        date_paragraph = Paragraph(f"Fecha: {current_date}", date_style)
        elements.append(date_paragraph)
        
        # Obtener datos organizados
        data = self._get_table_data()
        
        # Estilo base para las tablas
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        
        # Sección de Entradas
        title_style = ParagraphStyle(
            'CustomTitleStyle',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=30
        )
        elements.append(Paragraph("Entradas", title_style))
        
        if data['entradas']:
            headers = ["ID", "Tipo", "Monto", "Divisa", "Descripción", "Cuenta", "Fecha"]
            table_data = [headers] + data['entradas']
            t = Table(table_data)
            t.setStyle(table_style)
            elements.append(t)
        else:
            elements.append(Paragraph("No hay entradas registradas", self.styles['Normal']))
            
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Total Entradas: {data['total_entradas']}", self.styles['Normal']))
        elements.append(Spacer(1, 30))
        
        # Sección de Salidas
        elements.append(Paragraph("Salidas", title_style))
        
        if data['salidas']:
            table_data = [headers] + data['salidas']
            t = Table(table_data)
            t.setStyle(table_style)
            elements.append(t)
        else:
            elements.append(Paragraph("No hay salidas registradas", self.styles['Normal']))
            
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Total Salidas: {data['total_salidas']}", self.styles['Normal']))
        elements.append(Spacer(1, 30))
        
        # Balance Final
        elements.append(Paragraph(f"Balance Final: {data['balance']}", self.styles['Heading2']))
        
        # Generar el PDF
        doc.build(elements)

def generate_movement_report(tree_view):
    """
    Función helper para generar el reporte desde cualquier parte de la aplicación
    """
    # Obtener los datos del TreeView
    data = []
    for item in tree_view.get_children():
        values = tree_view.item(item)['values']
        data.append(values)
    
    # Crear el directorio de reportes si no existe
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generar nombre único para el archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reporte_movimientos_{timestamp}.pdf"
    output_path = os.path.join(reports_dir, filename)
    
    # Generar el PDF
    generator = PDFGenerator(data)
    generator.generate_pdf(output_path)
    
    return output_path