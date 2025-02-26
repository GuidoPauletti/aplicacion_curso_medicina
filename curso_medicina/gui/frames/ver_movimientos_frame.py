from curso_medicina.database.operations.movimiento_operations import get_movimientos_con_detalles
from ..utils.report_generator import generate_movement_report

from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import os

import customtkinter as ctk

class VerMovimientosFrame(ctk.CTkFrame):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.conn = conn
        self.setup_ui()

    def setup_ui(self):
        # Crear elementos de filtro
        self.label_filtro = ctk.CTkLabel(self, text="Ventana temporal:")
        self.label_filtro.pack(pady=5)

        self.frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtros.pack(pady=5)

        # Frame para la fecha "desde"
        self.frame_desde = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.frame_desde.pack(side="left", padx=10)
        self.label_desde = ctk.CTkLabel(self.frame_desde, text="Desde:")
        self.label_desde.pack(side="left", padx=5)
        self.fecha_desde = DateEntry(self.frame_desde, width=12, background='darkblue',
                                foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.fecha_desde.pack(side="left")
        self.fecha_desde.set_date(datetime.now() - timedelta(days=7))

        # Frame para la fecha "hasta"
        self.frame_hasta = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.frame_hasta.pack(side="left", padx=10)
        self.label_hasta = ctk.CTkLabel(self.frame_hasta, text="Hasta:")
        self.label_hasta.pack(side="left", padx=5)
        self.fecha_hasta = DateEntry(self.frame_hasta, width=12, background='darkblue',
                                foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.fecha_hasta.pack(side="left")
        self.fecha_hasta.set_date(datetime.now())

        # Botón para aplicar el filtro
        self.boton_filtrar = ctk.CTkButton(self.frame_filtros, text="Filtrar",
                                           command=lambda: self.filtrar_por_tiempo(self.fecha_desde.get_date(),
                                                                                   self.fecha_hasta.get_date()))
        self.boton_filtrar.pack(side="left", padx=10)

        # Crear tabla
        columnas = ("ID", "Tipo", "Monto", "Divisa", "Descripción", "Cuenta", "Fecha")
        
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", selectmode="browse")
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
        
        self.tabla.column("ID", width=50)
        self.tabla.column("Fecha", width=70)

        self.tabla.pack(fill="both", expand=True)

        # Frame para los botones
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(padx=10, pady=10)
        
        # Botones para cada divisa
        self.btn_pesos = ctk.CTkButton(
            self.buttons_frame,
            text="Informe",
            command=lambda: self.generate_report()
        )
        self.btn_pesos.grid(row=0, column=1, padx=5)

        # Obtener los movimientos
        self.cargar_movimientos(self.fecha_desde.get_date(), self.fecha_hasta.get_date())

    def cargar_movimientos(self, desde, hasta):
        # Limpiar tabla existente
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        movimientos = get_movimientos_con_detalles(self.conn, desde, hasta)
        for movimiento in movimientos:
            self.tabla.insert("", "end", values=movimiento)

    def filtrar_por_tiempo(self, desde, hasta):
    # Asegúrate de que la fecha "hasta" sea posterior a "desde"
        if hasta < desde:
            messagebox.showerror("Error", "La fecha 'hasta' debe ser posterior a la fecha 'desde'")
            return
        self.cargar_movimientos(desde, hasta)

    def generate_report(self):
        try:
            # Verificar si hay datos en la tabla
            if not self.tabla.get_children():
                messagebox.showwarning("Advertencia", "No hay datos para generar el informe")
                return
            
            # Generar el reporte
            output_path = generate_movement_report(self.tabla)

            # Verificar si el usuario seleccionó una ubicación
            if not output_path:
                return None  # El usuario canceló la selección
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Éxito", 
                f"Reporte generado exitosamente en:\n{output_path}"
            )
            
            # Abrir el archivo con el visor de PDF predeterminado
            os.startfile(output_path) if os.name == 'nt' else os.system(f'xdg-open "{output_path}"')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {str(e)}")