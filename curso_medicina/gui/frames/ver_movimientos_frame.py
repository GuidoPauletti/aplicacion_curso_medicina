from curso_medicina.database.operations.movimiento_operations import get_movimientos_con_detalles
from ..utils.report_generator import generate_movement_report

from tkinter import ttk, messagebox, simpledialog
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

        # Frame para los botones
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(padx=10, pady=10)
        
        # Botones para cada divisa
        self.btn_pesos = ctk.CTkButton(
            self.buttons_frame,
            text="Informe en Pesos",
            command=lambda: self.generate_report("Peso")
        )
        self.btn_pesos.grid(row=0, column=0, padx=5)
        
        self.btn_reales = ctk.CTkButton(
            self.buttons_frame,
            text="Informe en Reales",
            command=lambda: self.generate_report("Real")
        )
        self.btn_reales.grid(row=0, column=1, padx=5)
        
        self.btn_dolares = ctk.CTkButton(
            self.buttons_frame,
            text="Informe en Dólares",
            command=lambda: self.generate_report("Dolar")
        )
        self.btn_dolares.grid(row=0, column=3, padx=5)

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

    @staticmethod
    def ask_exchange_rate(divisa):
        """
        Solicita al usuario la tasa de cambio para la divisa seleccionada
        """
        if divisa.lower() in ['dolar', 'real']:
            rate = simpledialog.askfloat(
                "Tasa de Cambio",
                f"Ingrese la cantidad de pesos equivalente a 1 {divisa}:",
                minvalue=0.01
            )
            return rate
        return None

    def generate_report(self, divisa):
        try:
            # Verificar si hay datos en la tabla
            if not self.tabla.get_children():
                messagebox.showwarning("Advertencia", "No hay datos para generar el informe")
                return
            
            # Obtener tasa de cambio si es necesario
            exchange_rate = self.ask_exchange_rate(divisa)
            
            # Generar el reporte
            output_path = generate_movement_report(self.tabla, divisa, exchange_rate)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Éxito", 
                f"Reporte generado exitosamente en:\n{output_path}"
            )
            
            # Abrir el archivo con el visor de PDF predeterminado
            os.startfile(output_path) if os.name == 'nt' else os.system(f'xdg-open "{output_path}"')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {str(e)}")