from curso_medicina.database.operations.gasto_operations import insert_gasto
from curso_medicina.gui.utils.validators import validate_gasto_input

from tkinter import messagebox

import customtkinter as ctk


class AltaGastoFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, conn, usuario_actual):
        super().__init__(parent, width=400, height=500)
        self.conn = conn
        self.usuario_actual = usuario_actual
        self.setup_ui()

    def setup_ui(self):
        self.create_input_fields()
        self.create_save_button()

    def create_input_fields(self):
        # Label y Entry para monto
        self.label_monto = ctk.CTkLabel(self, text="Monto:")
        self.label_monto.pack(pady=5)
        self.entry_monto = ctk.CTkEntry(self, width=300)
        self.entry_monto.pack(pady=5)

        # Label y Entry para divisa
        self.label_divisa = ctk.CTkLabel(self, text="Divisa (Peso/Real):")
        self.label_divisa.pack(pady=5)
        self.divisa_var = ctk.StringVar()
        self.entry_divisa = ctk.CTkComboBox(self, variable=self.divisa_var,values=['Peso','Real','Dolar'],width=300)
        self.entry_divisa.pack(pady=5)

        # Label y Entry para correspondencia
        self.label_correspondencia = ctk.CTkLabel(self, text="Corresponde a:")
        self.label_correspondencia.pack(pady=5)
        self.entry_correspondencia = ctk.CTkEntry(self, width=300)
        self.entry_correspondencia.pack(pady=5)

        # Label y Entry para descripcion
        self.label_descripcion = ctk.CTkLabel(self, text="Descripción")
        self.label_descripcion.pack(pady = 5)
        self.entry_descripcion = ctk.CTkTextbox(self, width=300, height=200)
        self.entry_descripcion.pack(pady = 5)

    def create_save_button(self):
        self.btn_guardar = ctk.CTkButton(
            self, 
            text="Guardar Gasto",
            width=150,
            command=self.save_gasto
        )
        self.btn_guardar.pack(pady=20)

    def save_gasto(self):
        data = {
            'monto': self.entry_monto.get(),
            'divisa': self.entry_divisa.get(),
            'correspondencia': self.entry_correspondencia.get(),
            'descripcion': self.entry_descripcion.get("1.0", "end-1c"),
            'id_usuario': self.usuario_actual.id
        }
        
        if validate_gasto_input(data):
            gasto_id = insert_gasto(self.conn, **data)
            if gasto_id:
                messagebox.showinfo(
                    "Éxito",
                    f"Gasto ID {gasto_id} guardado correctamente"
                )
                self.clear_fields()
    
    def clear_fields(self):
        self.entry_monto.delete(0, 'end')
        self.entry_correspondencia.delete(0, 'end')
        self.entry_descripcion.delete("1.0", "end-1c")
        self.divisa_var.set("")