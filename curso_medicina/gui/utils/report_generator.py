# gui/utils/pdf_generator.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self, tree_data, exchange_rate = None):
        """
        Inicializa el generador de PDF con los datos del TreeView
        """
        self.tree_data = tree_data
        self.exchange_rate = exchange_rate
        self.styles = getSampleStyleSheet()
        # Definir anchos fijos para las columnas (en puntos)
        self.col_widths = [
            70,     # Monto
            240,    # Descripción
            100,    # Cuenta
            70      # Fecha
        ]

    @staticmethod
    def format_number(number):
        return "{:,.2f}".format(number).replace(",", "X").replace(".", ",").replace("X", ".")
        
    def _get_table_data(self):
        """
        Obtiene y organiza los datos de la tabla, separando entradas y salidas
        """
        entradas = []
        salidas = []
        total_entradas = 0
        total_salidas = 0
        
        for item in self.tree_data:
            row = list(item)
            # Formatear el monto para que siempre tenga 2 decimales
            row[2] = f"{float(row[2]):.2f}"
            row[2] = float(row[2])
            monto = row[2]
            row[2] = self.format_number(row[2])
            
            if row[1] == "Entrada":
                entradas.append([row[i] for i in(2,4,5,6)])
                total_entradas += float(monto)
            else:
                salidas.append([row[i] for i in(2,4,5,6)])
                total_salidas += float(monto)
                
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
        # Configurar el documento con márgenes específicos
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        elements = []
        
        # Estilo para la fecha
        date_style = ParagraphStyle(
            'CustomDateStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=20,
            alignment=0  # 0 = Izquierda
        )
        
        # Estilo para títulos
        title_style = ParagraphStyle(
            'CustomTitleStyle',
            parent=self.styles['Heading1'],
            fontSize=12,
            spaceAfter=10,
            alignment=0,  # 0 = Izquierda
            textTransform='uppercase'
        )
        
        # Estilo para totales
        total_style = ParagraphStyle(
            'TotalStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=20,
            alignment=0  # 0 = Izquierda
        )
        
        # Estilo base para las tablas - más minimalista y profesional
        table_style = TableStyle([
            # Encabezados
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            # Cuerpo de la tabla
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            # Alineación
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # ID centrado
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),   # Monto alineado a la derecha
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),    # Tipo alineado a la izquierda
            ('ALIGN', (3, 0), (6, -1), 'LEFT'),    # Resto de columnas a la izquierda
            # Líneas
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),  # Línea más gruesa bajo encabezados
        ])
        
        # Añadir fecha
        current_date = datetime.now().strftime("%d/%m/%Y")
        date_paragraph = Paragraph(f"Fecha: {current_date}", date_style)
        elements.append(date_paragraph)
        
        # Obtener datos organizados
        data = self._get_table_data()
        headers = ["Monto", "Descripción", "Cuenta", "Fecha"]
        
        # Sección de Entradas
        elements.append(Paragraph("Movimientos de Entrada", title_style))
        if data['entradas']:
            table_data = [headers] + data['entradas']
            t = Table(table_data, colWidths=self.col_widths)
            t.setStyle(table_style)
            elements.append(t)
        else:
            elements.append(Paragraph("No hay entradas registradas", self.styles['Normal']))
            
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(
            f"Total Entradas: {self.format_number(data['total_entradas'])}", 
            total_style
        ))
        elements.append(Spacer(1, 20))
        
        # Sección de Salidas
        elements.append(Paragraph("Movimientos de Salida", title_style))
        if data['salidas']:
            table_data = [headers] + data['salidas']
            t = Table(table_data, colWidths=self.col_widths)
            t.setStyle(table_style)
            elements.append(t)
        else:
            elements.append(Paragraph("No hay salidas registradas", self.styles['Normal']))
            
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(
            f"Total Salidas: {self.format_number(data['total_salidas'])}", 
            total_style
        ))
        elements.append(Spacer(1, 20))
        
        # Balance Final con línea separadora
        elements.append(Paragraph("_" * 50, ParagraphStyle(
            'Separator',
            parent=self.styles['Normal'],
            alignment=0
        )))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(
            f"Balance Final: {self.format_number(data['balance'])}",
            ParagraphStyle(
                'Balance',
                parent=self.styles['Normal'],
                fontSize=11,
                fontName='Helvetica-Bold'
            )
        ))

        # Agregar balance convertido a pesos si hay tasa de cambio
        if self.exchange_rate is not None:
            balance_pesos = data['balance'] * self.exchange_rate
            elements.append(Paragraph(
                f"Balance Final en Pesos: {self.format_number(balance_pesos)}",
                ParagraphStyle(
                    'BalancePesos',
                    parent=self.styles['Normal'],
                    fontSize=11,
                    fontName='Helvetica-Bold'
                )
            ))
        
        # Generar el PDF
        doc.build(elements)


def generate_movement_report(tree_view, divisa, exchange_rate = None):
    """
    Función helper para generar el reporte desde cualquier parte de la aplicación
    """
    # Obtener los datos del TreeView
    data = []
    for item in tree_view.get_children():
        values = tree_view.item(item)['values']
        if values[3] == divisa:  # El índice 3 corresponde a la columna de divisa
            data.append(values)
    
    # Crear el directorio de reportes si no existe
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generar nombre único para el archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reporte_movimientos_{timestamp}.pdf"
    output_path = os.path.join(reports_dir, filename)
    
    # Generar el PDF
    generator = PDFGenerator(data, exchange_rate)
    generator.generate_pdf(output_path)
    
    return output_path