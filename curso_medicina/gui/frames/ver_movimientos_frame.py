from curso_medicina.database.operations.movimiento_operations import get_movimientos_con_detalles
from ..utils.report_generator import generate_movement_report

from tkinter import ttk, messagebox
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
        
        self.optionmenu_correspondencia = ctk.CTkOptionMenu(
            self.frame_filtros,
            values=["Ultimo día", "Ultima semana", "Ultimo mes"],
            command=self.filtrar_por_tiempo
        )
        self.optionmenu_correspondencia.pack(side="left", padx=10)

        # Crear tabla
        columnas = ("ID", "Tipo", "Monto", "Divisa", "Descripción", "Cuenta", "Fecha")
        
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", selectmode="browse")
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
        
        self.tabla.column("ID", width=50)
        self.tabla.column("Fecha", width=70)

        self.tabla.pack(fill="both", expand=True)

        self.btn_editar = ctk.CTkButton(
            self, 
            text="Obtener informe", 
            command=self.generate_report
        )
        self.btn_editar.pack(pady=20)

        # Obtener los movimientos
        self.cargar_movimientos()

    def cargar_movimientos(self, ventana_temporal = "Ultimo día"):
        # Limpiar tabla existente
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        movimientos = get_movimientos_con_detalles(self.conn, ventana_temporal)
        for movimiento in movimientos:
            self.tabla.insert("", "end", values=movimiento)

    def filtrar_por_tiempo(self, ventana_temporal):
        self.cargar_movimientos(ventana_temporal)

    def generate_report(self):
        try:
            # Verificar si hay datos en la tabla
            if not self.tabla.get_children():
                messagebox.showwarning("Advertencia", "No hay datos para generar el informe")
                return
            
            # Generar el reporte
            output_path = generate_movement_report(self.tabla)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Éxito", 
                f"Reporte generado exitosamente en:\n{output_path}"
            )
            
            # Abrir el archivo con el visor de PDF predeterminado
            os.startfile(output_path) if os.name == 'nt' else os.system(f'xdg-open "{output_path}"')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {str(e)}")