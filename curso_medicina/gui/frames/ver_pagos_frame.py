from curso_medicina.gui.frames.base_frame import BaseFrame
from curso_medicina.database.operations.pagos_operations import get_pagos_con_detalles, borrar_pago, editar_pago

import customtkinter as ctk
from tkinter import ttk

class PagosFrame(ctk.CTkFrame):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.conn = conn
        self.setup_ui()

    def setup_ui(self):
        # Crear elementos de filtro
        self.label_filtro = ctk.CTkLabel(self, text="Filtrar por Correspondencia:")
        self.label_filtro.pack(pady=5)

        self.frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtros.pack(pady=5)
        
        self.optionmenu_correspondencia = ctk.CTkOptionMenu(
            self.frame_filtros,
            values=["Todos", "Fernanda", "Duanne"],
            command=self.filtrar_por_correspondencia
        )
        self.optionmenu_correspondencia.pack(side="left", padx=10)

        # Crear tabla
        columnas = ("ID", "Nombre", "Apellido", "Materia", "Monto", "Cuota", "Fecha")
        
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", selectmode="browse")
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
        
        self.tabla.column("ID", width=50)
        self.tabla.column("Cuota", width=50)
        self.tabla.column("Fecha", width=70)

        self.tabla.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tabla.pack(fill="both", expand=True)

        # Frame de botones
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(padx=10, pady=10)

        self.btn_borrar = ctk.CTkButton(
            self.buttons_frame, 
            text="Borrar Registro", 
            command=self.borrar_registro_pago,
            state="disabled"
        )
        self.btn_borrar.grid(row=0, column=0, padx=5)

        self.btn_editar = ctk.CTkButton(
            self.buttons_frame, 
            text="Editar Registro", 
            command=self.editar_registro_pago,
            state="disabled"
        )
        self.btn_editar.grid(row=0, column=1, padx=5)

        # Cargar datos iniciales
        self.cargar_pagos()

    def cargar_pagos(self, correspondencia="Todos"):
        # Limpiar tabla existente
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        # Traer info de pagos desde base de datos
        pagos = get_pagos_con_detalles(self.conn, correspondencia)
        for pago in pagos:
            self.tabla.insert("", "end", values=pago)

    def filtrar_por_correspondencia(self, correspondencia):
        self.cargar_pagos(correspondencia)

    def borrar_registro_pago(self):
        # Obtener el item seleccionado
        selected_item = self.tabla.selection()[0]
        pago_id = self.tabla.item(selected_item, "values")[0]
        if pago_id:
            borrado = borrar_pago(self.conn, pago_id)
            if borrado:
                self.tabla.delete(selected_item)

    def editar_registro_pago(self):
        # Obtener el item seleccionado
        selected_item = self.tabla.selection()[0]
        if selected_item:
            pago_data = self.tabla.item(selected_item, "values")
            self.ventana_editar_pago(pago_data, selected_item)

    def ventana_editar_pago(self, pago_data, selected_item):
        # Crear una nueva ventana para editar
        self.edit_window_pago = ctk.CTkToplevel(self)
        self.edit_window_pago.title("Editar Alumno")
        self.edit_window_pago.geometry("400x300")

        label_monto = ctk.CTkLabel(self.edit_window_pago, text="Monto")
        label_monto.pack(pady=5)
        entry_monto = ctk.CTkEntry(self.edit_window_pago)
        entry_monto.pack(pady=5)
        entry_monto.insert(0, pago_data[4])

        label_cuota = ctk.CTkLabel(self.edit_window_pago, text="Cuota")
        label_cuota.pack(pady=5)
        entry_cuota = ctk.CTkEntry(self.edit_window_pago)
        entry_cuota.pack(pady=5)
        entry_cuota.insert(0, pago_data[5])

        # Botón para guardar los cambios
        btn_guardar = ctk.CTkButton(self.edit_window_pago, text="Guardar", command=lambda: self.guardar_cambios_pago(selected_item, entry_monto.get(), entry_cuota.get(), pago_data))
        btn_guardar.pack(pady=10)

    def guardar_cambios_pago(self, selected_item, monto, cuota, pago_data):
        editado = editar_pago(self.conn, pago_data[0], monto, cuota)
        if editado:
            # Actualizar el registro en la tabla con los nuevos datos
            self.tabla.item(selected_item, values=(pago_data[0], pago_data[1], pago_data[2], pago_data[3], monto, cuota, pago_data[6]))
            self.edit_window_pago.destroy()

    def on_tree_select(self, event):
        selected_items = self.tabla.selection()
        self.btn_borrar.configure(state="normal" if selected_items else "disabled")
        self.btn_editar.configure(state="normal" if selected_items else "disabled")

