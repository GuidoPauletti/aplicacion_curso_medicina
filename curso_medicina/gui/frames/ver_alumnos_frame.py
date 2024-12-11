from curso_medicina.database.operations.alumno_operations import get_alumnos, editar_alumno, editar_dia_de_pago_alumno, get_inscripciones_alumno

import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

class VerAlumnosFrame(ctk.CTkFrame):
    def __init__(self, parent, conn, usuario_actual):
        super().__init__(parent)
        self.conn = conn
        self.usuario_actual = usuario_actual
        self.setup_ui()

    def setup_ui(self):
        self.label_filtro = ctk.CTkLabel(self, text="Filtrar por Materia:")
        self.label_filtro.pack(pady=5)
        
        self.optionmenu_materia = ctk.CTkOptionMenu(
            self, 
            values=["Todas", "Anatomia","Fisiologia","Farmacologia"] # Asocia el filtro con el método
        )
        self.optionmenu_materia.pack(pady=5)

        # Definir las columnas de la tabla
        columnas = ("ID","Nombre", "Apellido", "DNI", "Calle", "Numero", "Email", "Telefono")

        self.scrollable_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        self.scrollable_frame.pack(fill="both", expand=True)

        # Crear la tabla
        self.tabla_alumno = ttk.Treeview(self.scrollable_frame, columns=columnas, show="headings", selectmode="browse")
        for col in columnas:
            self.tabla_alumno.heading(col, text=col)

        self.tabla_alumno.tag_configure('deudor', background='red')
        self.tabla_alumno.column("ID", width=50, stretch=False)

        self.tabla_alumno.bind("<<TreeviewSelect>>", self.on_tree_select_alumno) # accion al seleccionar un registro

        self.tabla_alumno.pack(fill="both", expand=True)

        # Obtener los pagos desde la base de datos
        self.cargar_alumnos()

        # Crear frame para los botones debajo de la tabla
        self.buttons_frame_alumno = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame_alumno.pack(padx=10, pady=10)

        # Crear botón "Ver Alumno"
        self.btn_ver_detalle_alumno = ctk.CTkButton(self.buttons_frame_alumno, text="Ver Alumno", command=self.ver_detalle_alumno ,state="disabled")
        self.btn_ver_detalle_alumno.grid(row=0, column=0, padx=5)

        # Crear botón "Editar registro"
        self.btn_editar_alumno = ctk.CTkButton(self.buttons_frame_alumno, text="Editar Alumno", command=self.editar_alumno,state="disabled")
        self.btn_editar_alumno.grid(row=0, column=1, padx=5)

    def cargar_alumnos(self):
        # Obtener alumnos
        alumnos = get_alumnos(self.conn)

        for alumno in alumnos:
            if alumno[8] == "Si":
                self.tabla_alumno.insert("", tk.END, values=(alumno[0], alumno[1], alumno[2], alumno[3], alumno[4], alumno[5], alumno[6], alumno[7]), tags='deudor')
            else:
                self.tabla_alumno.insert("", tk.END, values=(alumno[0], alumno[1], alumno[2], alumno[3], alumno[4], alumno[5], alumno[6], alumno[7]))

    def on_tree_select_alumno(self, event):
        # Habilitar botones
        self.btn_ver_detalle_alumno.configure(state="normal")
        self.btn_editar_alumno.configure(state="normal")

    def ver_detalle_alumno(self):
        # Obtener el item seleccionado
        selected_item = self.tabla_alumno.selection()[0]
        datos_alumno = self.tabla_alumno.item(selected_item, "values")
        alumno_id = datos_alumno[0]
        if alumno_id:
            # Crear una nueva ventana para ver alumno
            self.vista_alumno = ctk.CTkToplevel(self)
            self.vista_alumno.title("Vista Alumno")
            self.vista_alumno.geometry("400x400")

            self.label_nombre_alumno = ctk.CTkLabel(self.vista_alumno, text=f"{datos_alumno[1]} {datos_alumno[2]}")
            self.label_nombre_alumno.pack(pady=5)

            # Definir las columnas de la tabla
            columnas_va = ("Materia", "Tipo de inscripcion", "Dia limite para pagar cada mes", "Deuda")

            self.frame_inscripciones_alumno = ctk.CTkFrame(self.vista_alumno)
            self.frame_inscripciones_alumno.pack(fill="both", expand=True)

            # Crear la tabla
            self.tabla_inscripciones_alumno = ttk.Treeview(self.frame_inscripciones_alumno, columns=columnas_va, show="headings", selectmode="browse")
            for col in columnas_va:
                self.tabla_inscripciones_alumno.heading(col, text=col)

            self.tabla_inscripciones_alumno.bind("<<TreeviewSelect>>", self.on_tree_select_incripcion_alumno) # accion al seleccionar un registro

            self.tabla_inscripciones_alumno.pack(fill="both", expand=True)

            # Obtener datos de inscripciones del alumno
            self.cargar_inscripcion_alumno(alumno_id)

            # Crear frame para los botones debajo de la tabla
            self.buttons_frame_inscripciones_alumno = ctk.CTkFrame(self.frame_inscripciones_alumno, fg_color="transparent")
            self.buttons_frame_inscripciones_alumno.pack(padx=10, pady=10)

            # Crear botón "Editar inscripcion"
            self.btn_ver_detalle_inscripcion_alumno = ctk.CTkButton(self.buttons_frame_inscripciones_alumno, text="Ver Alumno", command=lambda: print('ver inscripcion') ,state="disabled")
            self.btn_ver_detalle_inscripcion_alumno.grid(row=0, column=1, padx=5)

    def editar_alumno(self):
        # Obtener el item seleccionado
        selected_item = self.tabla_alumno.selection()[0]
        if selected_item:
            alumno_data = self.tabla_alumno.item(selected_item, "values")
            self.ventana_editar_alumno(alumno_data, selected_item)

    def ventana_editar_alumno(self, alumno_data, selected_item):
        self.edit_window_alumno_frame = ctk.CTkToplevel(self)
        self.edit_window_alumno_frame.title("Editar Alumno")
        self.edit_window_alumno_frame.geometry("400x600")
        self.edit_window_alumno = ctk.CTkScrollableFrame(self.edit_window_alumno_frame)
        self.edit_window_alumno.pack(fill="both", expand=True)

        label_nombre = ctk.CTkLabel(self.edit_window_alumno, text="Nombre")
        label_nombre.pack(pady=5)
        entry_nombre = ctk.CTkEntry(self.edit_window_alumno, width=300)
        entry_nombre.pack(pady=5)
        entry_nombre.insert(0, alumno_data[1])

        label_apellido = ctk.CTkLabel(self.edit_window_alumno, text="Apellido")
        label_apellido.pack(pady=5)
        entry_apellido = ctk.CTkEntry(self.edit_window_alumno, width=300)
        entry_apellido.pack(pady=5)
        entry_apellido.insert(0,alumno_data[2])

        label_dni = ctk.CTkLabel(self.edit_window_alumno, text="DNI")
        label_dni.pack(pady = 5)
        entry_dni = ctk.CTkEntry(self.edit_window_alumno, width=300)
        entry_dni.pack(pady = 5)
        entry_dni.insert(0,alumno_data[3])

        label_calle = ctk.CTkLabel(self.edit_window_alumno, text="Calle")
        label_calle.pack(pady = 5)
        entry_calle = ctk.CTkEntry(self.edit_window_alumno, width=300)
        entry_calle.pack(pady = 5)
        entry_calle.insert(0,alumno_data[4])

        label_numero = ctk.CTkLabel(self.edit_window_alumno, text="Numero")
        label_numero.pack(pady = 5)
        entry_numero = ctk.CTkEntry(self.edit_window_alumno, width=300)
        entry_numero.pack(pady = 5)
        entry_numero.insert(0,alumno_data[5])

        label_email = ctk.CTkLabel(self.edit_window_alumno, text="Email")
        label_email.pack(pady = 5)
        entry_email = ctk.CTkEntry(self.edit_window_alumno, width=300)
        entry_email.pack(pady = 5)
        entry_email.insert(0,alumno_data[6])

        label_telefono = ctk.CTkLabel(self.edit_window_alumno, text="Telefono")
        label_telefono.pack(pady = 5)
        entry_telefono = ctk.CTkEntry(self.edit_window_alumno, width=300)
        entry_telefono.pack(pady = 5)
        entry_telefono.insert(0,alumno_data[7])

        label_paga_el = ctk.CTkLabel(self.edit_window_alumno, text="Dia límite para pagar cada mes")
        label_paga_el.pack(pady = 5)
        entry_paga_el = ctk.CTkEntry(self.edit_window_alumno, width=300)
        entry_paga_el.pack(pady = 5)
        entry_paga_el.insert(0,'10')

        # Botón para guardar los cambios
        btn_guardar = ctk.CTkButton(self.edit_window_alumno, text="Guardar",
                                    command=lambda: self.guardar_cambios_alumno(selected_item,
                                                                                entry_nombre.get(),
                                                                                entry_apellido.get(),
                                                                                entry_dni.get(),
                                                                                entry_calle.get(),
                                                                                entry_numero.get(),
                                                                                entry_email.get(),
                                                                                entry_telefono.get(),
                                                                                entry_paga_el.get(),
                                                                                alumno_data))
        btn_guardar.pack(pady=10)

    def guardar_cambios_alumno(self, selected_item, nombre, apellido, dni, calle, numero, email, telefono, paga_el, alumno_data):
        editado = editar_alumno(self.conn, alumno_data[0], nombre, apellido, dni, calle, numero, email, telefono)
        editar_dia_de_pago_alumno(self.conn, alumno_data[0], paga_el)
        if editado:
            # Actualizar el registro en la tabla con los nuevos datos
            self.tabla_alumno.item(selected_item, values=(alumno_data[0], nombre, apellido, dni, calle, numero, email, telefono))
            self.edit_window_alumno_frame.destroy()

    def cargar_inscripcion_alumno(self, id_alumno):
        
        # Limpiar tabla existente
        for item in self.tabla_inscripciones_alumno.get_children():
            self.tabla_inscripciones_alumno.delete(item)

        inscripciones_alumno = get_inscripciones_alumno(self.conn, id_alumno)

        for inscripcion in inscripciones_alumno:
            self.tabla_inscripciones_alumno.insert("", tk.END, values=(inscripcion[0],inscripcion[1],inscripcion[2],inscripcion[3],))

    def on_tree_select_incripcion_alumno(self, event):
        self.btn_ver_detalle_inscripcion_alumno.configure(state="normal")