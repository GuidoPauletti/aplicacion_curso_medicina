from curso_medicina.database.operations.movimiento_operations import get_movimientos_con_detalles
from ..utils.report_generator import generate_movement_report

from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import os
import threading

import customtkinter as ctk

class VerMovimientosFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
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
        self.label_desde = ctk.CTkLabel(self.frame_desde, text="Desde (AAAA/MM/DD):")
        self.label_desde.pack(side="left", padx=5)
        self.fecha_desde_var = ctk.StringVar()
        self.fecha_desde = ctk.CTkEntry(self.frame_desde, textvariable = self.fecha_desde_var, placeholder_text="AAAA/MM/DD")
        self.fecha_desde.pack(pady=5)
        self.fecha_desde_var.set((datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))

        # Frame para la fecha "hasta"
        self.frame_hasta = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.frame_hasta.pack(side="left", padx=10)
        self.label_hasta = ctk.CTkLabel(self.frame_hasta, text="Hasta (AAAA/MM/DD):")
        self.label_hasta.pack(side="left", padx=5)
        self.fecha_hasta_var = ctk.StringVar()
        self.fecha_hasta = ctk.CTkEntry(self.frame_hasta, textvariable = self.fecha_hasta_var, placeholder_text="AAAA/MM/DD")
        self.fecha_hasta.pack(pady=5)
        self.fecha_hasta_var.set((datetime.now()).strftime("%Y-%m-%d"))

        # Botón para aplicar el filtro
        self.boton_filtrar = ctk.CTkButton(self.frame_filtros, text="Filtrar",
                                           command=lambda: self.filtrar_por_tiempo(self.fecha_desde_var.get(),
                                                                                   self.fecha_hasta_var.get()))
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
        threading.Thread(target= self.cargar_movimientos(self.fecha_desde_var.get(), self.fecha_hasta_var.get())
                         , daemon=True).start()

    def cargar_movimientos(self, desde, hasta):
        # Limpiar tabla existente
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        movimientos = get_movimientos_con_detalles(desde, hasta)
        for movimiento in movimientos:
            self.tabla.insert("", "end", values=movimiento)

    def filtrar_por_tiempo(self, desde, hasta):
    # Asegúrate de que la fecha "hasta" sea posterior a "desde"
        try:
            desde_f = datetime.strptime(desde, "%Y-%m-%d").date()
            hasta_f = datetime.strptime(hasta, "%Y-%m-%d").date()
            if hasta_f < desde_f:
                messagebox.showerror("Error", "La fecha 'hasta' debe ser posterior a la fecha 'desde'")
                return
        except:
            messagebox.showerror("Error", "No ha seleccionado un formato correcto de fecha (AAAA/MM/DD)")
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