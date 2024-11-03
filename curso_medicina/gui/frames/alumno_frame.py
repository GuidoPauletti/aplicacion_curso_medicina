from curso_medicina.database.operations.alumno_operations import insert_alumno
from curso_medicina.gui.utils.validators import validate_alumno_input

from tkinter import messagebox

import customtkinter as ctk


class AlumnoFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, conn):
        super().__init__(parent, width=400, height=500)
        self.conn = conn
        self.setup_ui()
        
    def setup_ui(self):
        self.create_input_fields()
        self.create_save_button()
    
    def create_input_fields(self):
        # Nombre
        self.label_nombre = ctk.CTkLabel(self, text="Nombre:")
        self.label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(self, width=300)
        self.entry_nombre.pack(pady=5)
        
        # Apellido
        self.label_apellido = ctk.CTkLabel(self, text="Apellido:")
        self.label_apellido.pack(pady=5)
        self.entry_apellido = ctk.CTkEntry(self, width=300)
        self.entry_apellido.pack(pady=5)
        
        # Teléfono
        self.label_telefono = ctk.CTkLabel(self, text="Teléfono:")
        self.label_telefono.pack(pady=5)
        self.entry_telefono = ctk.CTkEntry(self, width=300)
        self.entry_telefono.pack(pady=5)
    
    def create_save_button(self):
        self.btn_guardar = ctk.CTkButton(
            self, 
            text="Guardar Alumno",
            width=150,
            command=self.save_alumno
        )
        self.btn_guardar.pack(pady=20)
    
    def save_alumno(self):
        data = {
            'nombre': self.entry_nombre.get(),
            'apellido': self.entry_apellido.get(),
            'telefono': self.entry_telefono.get()
        }
        
        if validate_alumno_input(data):
            alumno_id = insert_alumno(self.conn, **data)
            if alumno_id:
                messagebox.showinfo(
                    "Éxito",
                    f"Alumno ID {alumno_id} guardado correctamente"
                )
                self.clear_fields()
                
    def clear_fields(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')