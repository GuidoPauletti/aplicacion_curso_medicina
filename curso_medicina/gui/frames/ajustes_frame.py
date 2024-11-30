from curso_medicina.database.operations.inscripcion_operations import get_info_inscripciones

from tkinter import ttk

import customtkinter as ctk


class AjustesFrame(ctk.CTkTabview):
    def __init__(self, parent, conn, usuario_actual):
        super().__init__(parent, width=400, height=500)
        self.conn = conn
        self.usuario_actual = usuario_actual
        self.add("Inscripciones")
        self.setup_ui()

    def setup_ui(self):
        
        # Inscripciones
        # Crear tabla
        columnas = ("ID", "Descripción", "Monto de cuota", "Monto de cuota con recargo", "Cantidad de cuotas")
        
        self.tabla = ttk.Treeview(self.tab("Inscripciones"), columns=columnas, show="headings", selectmode="browse")
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
        
        self.tabla.column("ID", width=50)

        self.tabla.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tabla.pack(fill="both", expand=True)

        # Frame de botones
        self.buttons_frame = ctk.CTkFrame(self.tab("Inscripciones"), fg_color="transparent")
        self.buttons_frame.pack(padx=10, pady=10)

        self.btn_crear = ctk.CTkButton(
            self.buttons_frame, 
            text="Crear Tipo de Inscripción", 
            command=lambda: print("crear")
        )
        self.btn_crear.grid(row=0, column=0, padx=5)

        self.btn_editar = ctk.CTkButton(
            self.buttons_frame, 
            text="Editar Inscripción", 
            command=lambda: print("editar"),
            state="disabled"
        )
        self.btn_editar.grid(row=0, column=1, padx=5)

        # Cargar datos iniciales
        self.cargar_tipo_inscripciones()

    def cargar_tipo_inscripciones(self):
        # Limpiar tabla existente
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Traer info de pagos desde base de datos
        tipos_inscripcion = get_info_inscripciones(self.conn)
        for tipo in tipos_inscripcion:
            self.tabla.insert("", "end", values=tipo)

    def on_tree_select(self, event):
        selected_items = self.tabla.selection()
        self.btn_editar.configure(state="normal" if selected_items else "disabled")