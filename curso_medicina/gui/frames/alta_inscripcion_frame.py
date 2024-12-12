from curso_medicina.database.operations.alumno_operations import get_alumnos, insert_alumno_materia
from curso_medicina.database.operations.materia_operations import get_materias_por_alumno
from curso_medicina.database.operations.inscripcion_operations import get_descripciones, get_detalle_tipo_inscripcion, save_tipo_inscripcion

from tkinter import messagebox

import customtkinter as ctk


class AltaInscripcionFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, conn, usuario_actual):
        super().__init__(parent, width=400, height=500)
        self.conn = conn
        self.usuario_actual = usuario_actual
        self.setup_ui()

    def setup_ui(self):
        self.create_input_fields()
        self.create_save_button()

    def create_input_fields(self):
        # Obtener lista de alumnos
        self.alumnos = get_alumnos(self.conn)

        # Label y Combobox para seleccionar alumno
        label_alumno = ctk.CTkLabel(self, text="Seleccionar Alumno:")
        label_alumno.pack(pady=5)
        
        self.alumno_var = ctk.StringVar()
        self.combobox_alumno = ctk.CTkComboBox(self, variable=self.alumno_var, width=300)

        self.combobox_alumno.pack(pady=5)
        self.actualizar_combobox("")  # Inicializa la lista completa

        # Evento para filtrar nombres mientras se escribe en el ComboBox
        self.combobox_alumno.bind('<KeyRelease>', self.filtrar_alumnos)

        # Materias
        self.create_checkboxes_materias()

        # Tipo Inscripcion
        self.label_inscripcion = ctk.CTkLabel(self, text="Tipo Inscripción:")
        self.label_inscripcion.pack(pady=5)
        self.inscripcion_var = ctk.StringVar()
        self.inscripcion_var.set("1 - regular")

        # obtenemos los valores para el dropdown de inscripciones
        self.tipo_inscripciones = self.get_tipo_inscripciones()
        self.lista_inscripciones = [f"{inscripcion[0]} - {inscripcion[1]}" for inscripcion in self.tipo_inscripciones] + ["Otro"]

        self.combobox_inscripcion = ctk.CTkOptionMenu(self,
                                                    variable=self.inscripcion_var,
                                                    values=self.lista_inscripciones,
                                                    width=300,
                                                    command=self.display_info_inscripcion)
        self.combobox_inscripcion.pack(pady=5)

        # Mostrar la informacion del tipo de inscripcion
        self.label_info_inscripcion = ctk.CTkLabel(self, text="", text_color="#0066ff")
        self.label_info_inscripcion.pack(pady=3)
        self.display_info_inscripcion(event=None)

    def actualizar_combobox(self, filtro):
        # Filtra la lista de alumnos por el filtro (ignora mayúsculas/minúsculas)
        alumnos_filtrados = [f"{alumno[0]} - {alumno[1]} {alumno[2]}" for alumno in self.alumnos if alumno[1].lower().startswith(filtro.lower())]
        self.combobox_alumno.configure(values=alumnos_filtrados)

    def filtrar_alumnos(self, event):
        filtro = self.combobox_alumno.get()
        self.actualizar_combobox(filtro)

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
            text="Confirmar inscripción",
            width=150,
            command=self.save_inscripcion
        )
        self.btn_guardar.pack(pady=20)
    
    def save_inscripcion(self):
        alumno = self.alumno_var.get()
        seleccion_materias = self.get_materias_seleccionadas()
        if alumno == "":
            messagebox.showerror(
                title="Error",
                message="Debe seleccionar un alumno"
            )
            return
        elif len(seleccion_materias) == 0:
            messagebox.showerror(
                title="Error",
                message="Debe seleccionar al menos una materia"
            )
            return
        else:
            alumno_id = int(alumno.split(" - ")[0])
            tipo_inscripcion = self.inscripcion_var.get()
            inscripcion_id = int(tipo_inscripcion.split(" - ")[0])
            self.save_alumno_materia(alumno_id, seleccion_materias, inscripcion_id)
            self.clear_fields()

    def get_tipo_inscripciones(self):
        inscripciones = get_descripciones(self.conn)
        return inscripciones
    
    def display_info_inscripcion(self, event):
        tipo_inscripcion = self.inscripcion_var.get()
        if tipo_inscripcion != "Otro":
            tipo_inscripcion_id = int(tipo_inscripcion.split(" - ")[0])
            info_tipo_inscripcion = get_detalle_tipo_inscripcion(self.conn, tipo_inscripcion_id)
            monto = info_tipo_inscripcion[2]
            monto_recargo = info_tipo_inscripcion[3]
            n_cuotas = info_tipo_inscripcion[4]
            string_tipo_inscripcion = f"{n_cuotas} cuotas de ${monto} o ${monto_recargo} con recargo"
            self.label_info_inscripcion.configure(text=string_tipo_inscripcion)
            return
        else:
            self.ventana_crear_tipo_inscripcion()

    def ventana_crear_tipo_inscripcion(self):
        # Crear una nueva ventana para crear tipo de inscripcion
        self.create_window_inscripcion = ctk.CTkToplevel(self)
        self.create_window_inscripcion.title("Crear tipo de inscripción")
        self.create_window_inscripcion.geometry("500x500")

        label_descripcion = ctk.CTkLabel(self.create_window_inscripcion, text="Descripción")
        label_descripcion.pack(pady=5)
        entry_descripcion = ctk.CTkEntry(self.create_window_inscripcion, width=300)
        entry_descripcion.pack(pady=5)
        entry_descripcion.insert(0,"Descripción breve del tipo de incripción")

        label_cuota = ctk.CTkLabel(self.create_window_inscripcion, text="Monto cuota")
        label_cuota.pack(pady=5)
        entry_cuota = ctk.CTkEntry(self.create_window_inscripcion)
        entry_cuota.pack(pady=5)

        label_cuota_recargo = ctk.CTkLabel(self.create_window_inscripcion, text="Monto cuota con recargo")
        label_cuota_recargo.pack(pady=5)
        entry_cuota_recargo = ctk.CTkEntry(self.create_window_inscripcion)
        entry_cuota_recargo.pack(pady=5)

        label_n_cuotas = ctk.CTkLabel(self.create_window_inscripcion, text="Numero de cuotas")
        label_n_cuotas.pack(pady=5)
        entry_n_cuotas = ctk.CTkEntry(self.create_window_inscripcion)
        entry_n_cuotas.pack(pady=5)

        # Botón para guardar los cambios
        btn_guardar = ctk.CTkButton(self.create_window_inscripcion,
                                    text="Guardar",
                                    command=lambda: self.guardar_tipo_inscripcion(
                                        descripcion = entry_descripcion.get(),
                                        cuota = entry_cuota.get(),
                                        cuota_recargo = entry_cuota_recargo.get(),
                                        n_cuotas = entry_n_cuotas.get()
                                    ))
        btn_guardar.pack(pady=10)

    def guardar_tipo_inscripcion(self, descripcion, cuota, cuota_recargo, n_cuotas):
        nuevo_tipo_incripcion = save_tipo_inscripcion(self.conn, descripcion, cuota, cuota_recargo, n_cuotas)
        if nuevo_tipo_incripcion:
            self.lista_inscripciones = self.lista_inscripciones[:-1] + [f"{nuevo_tipo_incripcion} - {descripcion}", "Otro"]
            self.combobox_inscripcion.configure(values=self.lista_inscripciones)
            self.inscripcion_var.set(f"{nuevo_tipo_incripcion} - {descripcion}")
            self.display_info_inscripcion(event=None)
            self.create_window_inscripcion.destroy()
        else:
            return
        
    def save_alumno_materia(self, alumno_id, seleccion_materias, inscripcion_id):
        materias_ya_inscripto = get_materias_por_alumno(self.conn, alumno_id)
        materias_ya_inscripto_id = [materia[0] for materia in materias_ya_inscripto]
        for materia_id in seleccion_materias:
            if materia_id in materias_ya_inscripto_id:
                messagebox.showwarning(
                    "Rechazado",
                    f"El alumno ID {alumno_id} ya está inscripto a la materia ID {materia_id}"
                )
            else:
                insert_alumno_materia(self.conn, alumno_id, materia_id, inscripcion_id)
                messagebox.showinfo(
                    "Éxito",
                    f"Alumno ID {alumno_id} inscripto correctamente a la materia de ID {materia_id}"
                )
        

    def clear_fields(self):
        self.alumno_var.set("")
        self.inscripcion_var.set("1 - regular")