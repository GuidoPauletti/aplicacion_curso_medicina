from curso_medicina.database.operations.alumno_operations import insert_alumno, insert_alumno_materia
from curso_medicina.database.operations.inscripcion_operations import get_descripciones
from curso_medicina.gui.utils.validators import validate_alumno_input


from tkinter import messagebox

import customtkinter as ctk


class AltaAlumnoFrame(ctk.CTkScrollableFrame):
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
        self.create_checkboxes_materias()

        # Tipo Inscripcion
        self.label_inscripcion = ctk.CTkLabel(self, text="Tipo Inscripción:")
        self.label_inscripcion.pack(pady=5)
        self.inscripcion_var = ctk.StringVar()
        self.inscripcion_var.set("regular")

        # obtenemos los valores para el dropdown de inscripciones
        self.tipo_inscripciones = self.get_tipo_inscripciones()
        lista_inscripciones = [f"{inscripcion[0]} - {inscripcion[1]}" for inscripcion in self.tipo_inscripciones]

        self.combobox_inscripcion = ctk.CTkComboBox(self, variable=self.inscripcion_var,values=lista_inscripciones,width=300)
        self.combobox_inscripcion.pack(pady=5)

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


    def create_checkboxes_materias(self):
        """
        Crea los checkboxes de materias en el frame proporcionado.
        """
        self.label_materias = ctk.CTkLabel(self, text="Materias:")
        self.label_materias.pack(pady=5)

        # Frame horizontal para los checkboxes
        self.checkbox_frame_u = ctk.CTkFrame(self, fg_color="transparent")
        self.checkbox_frame_u.pack(pady=5)
        self.checkbox_frame_l = ctk.CTkFrame(self, fg_color="transparent")
        self.checkbox_frame_l.pack(pady=5)

        # Valores para verificar si la materia está seleccionada
        self.var_anatomia = ctk.BooleanVar()
        self.var_fisiologia = ctk.BooleanVar()
        self.var_bioquimica = ctk.BooleanVar()
        self.var_inmunologia = ctk.BooleanVar()
        self.var_microbiologia = ctk.BooleanVar()
        self.var_farmacologia = ctk.BooleanVar()
        self.var_patologia = ctk.BooleanVar()

        materias = self.get_materias_cbx_config()

        for i, materia in enumerate(materias):
            checkbox = ctk.CTkCheckBox(
                self.checkbox_frame_u if i < len(materias)//2 else self.checkbox_frame_l,
                text=materia["text"],
                variable=materia["var"]
            )
            checkbox.pack(side="left", padx=10)


    def get_materias_cbx_config(self) -> list:
        return [
            {"text": "Anatomía", "var": self.var_anatomia, "id": 1},
            {"text": "Fisiología", "var": self.var_fisiologia, "id": 2},
            {"text": "Bioquímica", "var": self.var_bioquimica, "id": 3},
            {"text": "Inmunología", "var": self.var_inmunologia, "id": 4},
            {"text": "Microbiología", "var": self.var_microbiologia, "id": 5},
            {"text": "Farmacología", "var": self.var_farmacologia, "id": 6},
            {"text": "Patología", "var": self.var_patologia, "id": 7}
        ]
    
    def get_materias_seleccionadas(self) -> list:
        materias = self.get_materias_cbx_config()
        materias_seleccionadas = []
        for materia in materias:
            if materia["var"].get():
                materias_seleccionadas.append(materia["id"])
        return materias_seleccionadas
    
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
                # Inscribimos el alumno a la materia
                seleccion_materias = self.get_materias_seleccionadas()
                tipo_inscripcion = self.inscripcion_var.get()
                inscripcion_id = int(tipo_inscripcion.split(" - ")[0])
                self.save_alumno_materia(alumno_id, seleccion_materias, inscripcion_id)
                self.clear_fields()
                
    def save_alumno_materia(self, alumno_id, seleccion_materias, inscripcion_id):
        for materia_id in seleccion_materias:
            insert_alumno_materia(self.conn, alumno_id, materia_id, inscripcion_id)

    def get_tipo_inscripciones(self):
        inscripciones = get_descripciones(self.conn)
        return inscripciones

    def clear_fields(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        self.entry_dni.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_dir_calle.delete(0, 'end')
        self.entry_dir_numero.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')