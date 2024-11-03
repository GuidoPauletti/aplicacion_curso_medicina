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

        # Materias
        self.label_materias = ctk.CTkLabel(self, text="Materias:")
        self.label_materias.pack(pady=5)
        
        ## Frame horizontal para los checkboxes
        self.checkbox_frame_u = ctk.CTkFrame(self, fg_color="transparent")
        self.checkbox_frame_u.pack(pady=5)

        self.checkbox_frame_l = ctk.CTkFrame(self, fg_color="transparent")
        self.checkbox_frame_l.pack(pady=5)

        ## Checkboxes para materias
        self.var_anatomia = ctk.BooleanVar()
        self.var_fisiologia = ctk.BooleanVar()
        self.var_bioquimica = ctk.BooleanVar()
        self.var_inmunologia = ctk.BooleanVar()
        self.var_microbiologia = ctk.BooleanVar()
        self.var_farmacologia = ctk.BooleanVar()
        self.var_patologia = ctk.BooleanVar()
        
        self.checkbox_anatomia = ctk.CTkCheckBox(self.checkbox_frame_u, text="Anatomía", 
                                          variable=self.var_anatomia)
        self.checkbox_anatomia.pack(side="left", padx=10)
        
        self.checkbox_fisiologia = ctk.CTkCheckBox(self.checkbox_frame_u, text="Fisiología", 
                                            variable=self.var_fisiologia)
        self.checkbox_fisiologia.pack(side="left", padx=10)
        
        self.checkbox_bioquimica = ctk.CTkCheckBox(self.checkbox_frame_u, text="Bioquimica", 
                                             variable=self.var_bioquimica)
        self.checkbox_bioquimica.pack(side="left", padx=10)

        self.checkbox_inmunologia = ctk.CTkCheckBox(self.checkbox_frame_l, text="Inmunologia", 
                                             variable=self.var_inmunologia)
        self.checkbox_inmunologia.pack(side="left", padx=10)

        self.checkbox_microbiologia = ctk.CTkCheckBox(self.checkbox_frame_l, text="Microbiologia", 
                                             variable=self.var_microbiologia)
        self.checkbox_microbiologia.pack(side="left", padx=10)

        self.checkbox_farmacologia = ctk.CTkCheckBox(self.checkbox_frame_l, text="Farmacologia", 
                                             variable=self.var_farmacologia)
        self.checkbox_farmacologia.pack(side="left", padx=10)

        self.checkbox_patologia = ctk.CTkCheckBox(self.checkbox_frame_l, text="Patologia", 
                                             variable=self.var_patologia)
        self.checkbox_patologia.pack(side="left", padx=10)

        # DNI
        self.label_dni = ctk.CTkLabel(self, text="DNI:")
        self.label_dni.pack(pady=5)
        self.entry_dni = ctk.CTkEntry(self, width=300)
        self.entry_dni.pack(pady=5)

        # Email
        self.label_email = ctk.CTkLabel(self, text="Email:")
        self.label_email.pack(pady=5)
        self.entry_email = ctk.CTkEntry(self, width=300)
        self.entry_email.pack(pady=5)
        
        # Teléfono
        self.label_telefono = ctk.CTkLabel(self, text="Teléfono:")
        self.label_telefono.pack(pady=5)
        self.entry_telefono = ctk.CTkEntry(self, width=300)
        self.entry_telefono.pack(pady=5)

        # Calle
        self.label_dir_calle = ctk.CTkLabel(self, text="Dirección - Calle:")
        self.label_dir_calle.pack(pady=5)
        self.entry_dir_calle = ctk.CTkEntry(self, width=300)
        self.entry_dir_calle.pack(pady=5)

        # Numero
        self.label_dir_numero = ctk.CTkLabel(self, text="Dirección - Número:")
        self.label_dir_numero.pack(pady=5)
        self.entry_dir_numero = ctk.CTkEntry(self, width=300)
        self.entry_dir_numero.pack(pady=5)
    
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
            'dni': self.entry_dni.get(),
            'email': self.entry_email.get(),
            'telefono': self.entry_telefono.get(),
            'dir_calle': self.entry_dir_calle.get(),
            'dir_numero': self.entry_dir_numero.get()
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