from datetime import datetime
from tkinter import filedialog

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class PDFGenerator:
    def __init__(self, tree_data):
        """
        Inicializa el generador de PDF con los datos del TreeView
        """
        self.tree_data = tree_data
        self.styles = getSampleStyleSheet()
        # Definir anchos fijos para las columnas (en puntos)
        self.col_widths = [
            70,     # Monto
            75,     # Divisa
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
        total_entradas_reales = 0
        total_entradas_dolares = 0
        total_salidas = 0
        total_salidas_reales = 0
        total_salidas_dolares = 0
        
        for item in self.tree_data:
            row = list(item)
            # Formatear el monto para que siempre tenga 2 decimales
            row[2] = f"{float(row[2]):.2f}"
            row[2] = float(row[2])
            monto = row[2]
            row[2] = self.format_number(row[2])
            
            if row[1] == "Entrada":
                entradas.append([row[i] for i in(2,3,4,5,6)])
                if row[3].startswith("Peso"):
                    total_entradas += float(monto)
                elif row[3].startswith("Real"):
                    total_entradas_reales += float(monto)
                elif row[3].startswith("Dolar"):
                    total_entradas_dolares += float(monto)
            else:
                salidas.append([row[i] for i in(2,3,4,5,6)])
                if row[3].startswith("Peso"):
                    total_salidas += float(monto)
                elif row[3].startswith("Real"):
                    total_salidas_reales += float(monto)
                elif row[3].startswith("Dolar"):
                    total_salidas_dolares += float(monto)
                
        return {
            'entradas': entradas,
            'salidas': salidas,
            'total_entradas': total_entradas,
            'total_entradas_reales': total_entradas_reales,
            'total_entradas_dolares': total_entradas_dolares,
            'total_salidas': total_salidas,
            'total_salidas_reales': total_salidas_reales,
            'total_salidas_dolares': total_salidas_dolares,
            'balance': total_entradas - total_salidas,
            'balance_reales': total_entradas_reales - total_salidas_reales,
            'balance_dolares': total_entradas_dolares - total_salidas_dolares
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
        headers = ["Monto", "Divisa", "Descripción", "Cuenta", "Fecha"]
        
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

        if data['total_entradas_reales'] > 0:
            elements.append(Paragraph(
                f"Total Entradas en Reales: {self.format_number(data['total_entradas_reales'])} R$", 
                total_style
            ))
            elements.append(Spacer(1, 1))
        
        if data['total_entradas_dolares'] > 0:
            elements.append(Paragraph(
                f"Total Entradas en Dolares: {self.format_number(data['total_entradas_dolares'])} USD$", 
                total_style
            ))
            elements.append(Spacer(1, 1))

        if data['total_entradas'] > 0:
            elements.append(Paragraph(
                f"Total Entradas en Pesos: {self.format_number(data['total_entradas'])} ARS$", 
                total_style
            ))
            elements.append(Spacer(1, 3))

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

        if data['total_salidas_reales'] > 0:
            elements.append(Paragraph(
                f"Total Salidas en Reales: {self.format_number(data['total_salidas_reales'])} R$", 
                total_style
            ))
            elements.append(Spacer(1, 1))

        if data['total_salidas_dolares'] > 0:
            elements.append(Paragraph(
                f"Total Salidas en Dolares: {self.format_number(data['total_salidas_dolares'])} USD$", 
                total_style
            ))
            elements.append(Spacer(1, 1))

        if data['total_salidas'] > 0:
            elements.append(Paragraph(
                f"Total Salidas: {self.format_number(data['total_salidas'])} ARS$", 
                total_style
            ))
            elements.append(Spacer(1, 5))
        
        # Balance Final con línea separadora
        elements.append(Paragraph("_" * 50, ParagraphStyle(
            'Separator',
            parent=self.styles['Normal'],
            alignment=0
        )))
        elements.append(Spacer(1, 10))

        if data['total_entradas'] > 0 or data['total_salidas'] > 0:
            elements.append(Paragraph(
                f"Balance Final en Pesos: {self.format_number(data['balance'])} ARS$",
                ParagraphStyle(
                    'Balance',
                    parent=self.styles['Normal'],
                    fontSize=11,
                    fontName='Helvetica-Bold'
                )
            ))
            elements.append(Spacer(1, 5))

        if data['total_entradas_reales'] > 0 or data['total_salidas_reales'] > 0:
            elements.append(Paragraph(
                f"Balance Final en Reales: {self.format_number(data['balance_reales'])} R$",
                ParagraphStyle(
                    'Balance',
                    parent=self.styles['Normal'],
                    fontSize=11,
                    fontName='Helvetica-Bold'
                )
            ))
            elements.append(Spacer(1, 5))

        if data['total_entradas_dolares'] > 0 or data['total_salidas_dolares'] > 0:
            elements.append(Paragraph(
                f"Balance Final en Dolares: {self.format_number(data['balance_dolares'])} USD$",
                ParagraphStyle(
                    'Balance',
                    parent=self.styles['Normal'],
                    fontSize=11,
                    fontName='Helvetica-Bold'
                )
            ))
            elements.append(Spacer(1, 5))
        
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
    
    
    # Generar nombre único para el archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"reporte_movimientos_{timestamp}.pdf"
    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=default_filename
    )
    
    # Verificar si el usuario seleccionó una ubicación
    if not output_path:
        return None  # El usuario canceló la selección

    # Generar el PDF
    generator = PDFGenerator(data)
    generator.generate_pdf(output_path)
    
    return output_path