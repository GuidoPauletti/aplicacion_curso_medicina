from curso_medicina.database.operations.alumno_operations import get_alumnos, editar_alumno, editar_dia_de_pago_alumno, get_inscripciones_alumno, get_alumnos_por_materia, get_unico_alumno, get_alumnos_filtrados
from curso_medicina.database.operations.deuda_operations import perdonar_deuda_inscripcion
from curso_medicina.database.operations.inscripcion_operations import editar_inscripcion, get_descripciones

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import threading

import customtkinter as ctk

class VerAlumnosFrame(ctk.CTkFrame):
    def __init__(self, parent, usuario_actual):
        super().__init__(parent)
        self.usuario_actual = usuario_actual

        # Variables de paginación
        self.pagina_actual = 1
        self.registros_por_pagina = 20
        self.total_registros = 0
        self.total_paginas = 0
        
        # Variables para manejo de hilos
        self.loading = False
        self.carga_cancelada = False

        self.setup_ui()

    def setup_ui(self):
        # Crear elementos de filtro
        self.frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtros.pack(pady=5)

        self.label_filtro = ctk.CTkLabel(self.frame_filtros, text="Filtrar por Materia:")
        self.label_filtro.grid(row=0, column=0, padx=5)
        
        self.optionmenu_materia = ctk.CTkOptionMenu(
            self.frame_filtros, 
            values=["Todas","Anatomia","Fisiologia","Bioquimica","Inmunologia","Microbiologia","Farmacologia","Patologia"],
            command= self.filtrar_alumnos_por_materia
        )
        self.optionmenu_materia.grid(row=1, column=0, padx=5)

        self.label_filtro_alumno = ctk.CTkLabel(self.frame_filtros, text="Buscar por nombre o apellido:")
        self.label_filtro_alumno.grid(row=0, column=1, padx=5)

        # Obtener lista de alumnos
        self.alumnos = get_alumnos()
        self.alumnos = self.alumnos[0]

        self.alumno_var = ctk.StringVar()
        self.optionmenu_alumno = ctk.CTkComboBox(
            self.frame_filtros,
            variable=self.alumno_var,
            command=self.filtrar_por_alumno
        )
        self.optionmenu_alumno.grid(row=1, column=1, padx=5)

        self.actualizar_combobox(self.alumnos[:10])  # Inicializa la lista completa

        # Evento para filtrar nombres mientras se escribe en el ComboBox
        self.optionmenu_alumno.bind('<KeyRelease>', self.filtrar_alumnos)

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

        # Frame para paginación
        self.paginacion_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.paginacion_frame.pack(fill="x", padx=10, pady=5)
        
        # Botones de paginación
        self.btn_anterior = ctk.CTkButton(self.paginacion_frame, text="Anterior", command=self.pagina_anterior)
        self.btn_anterior.pack(side="left", padx=5)
        
        self.lbl_pagina = ctk.CTkLabel(self.paginacion_frame, text="Página 0 de 0")
        self.lbl_pagina.pack(side="left", padx=10)
        
        self.btn_siguiente = ctk.CTkButton(self.paginacion_frame, text="Siguiente", command=self.pagina_siguiente)
        self.btn_siguiente.pack(side="left", padx=5)
        
        # Selector de registros por página
        self.lbl_por_pagina = ctk.CTkLabel(self.paginacion_frame, text="Registros por página: 20")
        self.lbl_por_pagina.pack(side="left", padx=10)
        
        # Botón de actualizar
        self.btn_actualizar = ctk.CTkButton(self.paginacion_frame, text="Actualizar", command=self.cargar_alumnos)
        self.btn_actualizar.pack(side="right", padx=10)
        
        # Indicador de carga
        self.lbl_cargando = ctk.CTkLabel(self, text="")
        self.lbl_cargando.pack(pady=5)

        # Crear frame para los botones debajo de la tabla
        self.buttons_frame_alumno = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame_alumno.pack(padx=10, pady=10)

        # Crear botón "Ver Alumno"
        self.btn_ver_detalle_alumno = ctk.CTkButton(self.buttons_frame_alumno, text="Ver Inscripciones", command=self.ver_detalle_alumno ,state="disabled")
        self.btn_ver_detalle_alumno.grid(row=0, column=0, padx=5)

        # Crear botón "Editar registro"
        self.btn_editar_alumno = ctk.CTkButton(self.buttons_frame_alumno, text="Editar Alumno", command=self.editar_alumno,state="disabled")
        self.btn_editar_alumno.grid(row=0, column=1, padx=5)

        # Obtener los alumnos desde la base de datos
        self.cargar_alumnos()

    def cargar_alumnos(self):
        """Carga los datos de la página actual"""
        if self.loading:
            self.carga_cancelada = True
            self.lbl_cargando.configure(text="Cancelando carga anterior...")
            return
        
        self.carga_cancelada = False
        self.loading = True
        self.lbl_cargando.configure(text=f"Cargando datos...")

        # Limpiar tabla existente
        for item in self.tabla_alumno.get_children():
            self.tabla_alumno.delete(item)        

        # Deshabilitar controles durante la carga
        self.btn_anterior.configure(state="disabled")
        self.btn_siguiente.configure(state="disabled")
        self.btn_actualizar.configure(state="disabled")

        # Iniciar hilo de carga
        thread = threading.Thread(target=self.cargar_alumnos_thread, daemon=True)
        thread.start()

    def cargar_alumnos_thread(self):
        materia = self.optionmenu_materia.get()
        try:
            alumnos, total = get_alumnos_por_materia(materia, self.pagina_actual, self.registros_por_pagina)
            if self.carga_cancelada:
                return
            
            # Actualizar información de paginación
            self.total_registros = total
            self.total_paginas = (total + self.registros_por_pagina - 1) // self.registros_por_pagina

            # Actualizar interfaz en el hilo principal
            self.after(0, lambda: self.mostrar_alumnos(alumnos))
            self.after(0, self.actualizar_controles_paginacion)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Error al cargar alumnos: {e}"))
        
        finally:
            self.after(0, lambda: self.lbl_cargando.configure(text="Datos cargados"))
            self.after(0, lambda: setattr(self, 'loading', False))
            self.after(0, lambda: self.btn_actualizar.configure(state="normal"))

    def mostrar_alumnos(self, alumnos):
        for alumno in alumnos:
            if alumno[8] == "Si":
                self.tabla_alumno.insert("", tk.END, values=(alumno[0], alumno[1], alumno[2], alumno[3], alumno[4], alumno[5], alumno[6], alumno[7]), tags='deudor')
            else:
                self.tabla_alumno.insert("", tk.END, values=(alumno[0], alumno[1], alumno[2], alumno[3], alumno[4], alumno[5], alumno[6], alumno[7]))

    def actualizar_controles_paginacion(self):
        """Actualiza los controles de paginación"""
        # Actualizar etiqueta de página
        self.lbl_pagina.configure(text=f"Página {self.pagina_actual} de {self.total_paginas} ({self.total_registros} registros)")
        
        # Habilitar/deshabilitar botones según corresponda
        self.btn_anterior.configure(state="normal" if self.pagina_actual > 1 else "disabled")
        self.btn_siguiente.configure(state="normal" if self.pagina_actual < self.total_paginas else "disabled")

    def pagina_anterior(self):
        """Navega a la página anterior"""
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.cargar_alumnos()
    
    def pagina_siguiente(self):
        """Navega a la página siguiente"""
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.cargar_alumnos()
    
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
            self.vista_alumno = Toplevel(self)
            self.vista_alumno.title("Inscripciones de Alumno")
            self.vista_alumno.geometry("1050x400")

            self.vista_alumno.transient()
            self.vista_alumno.grab_set()

            self.label_nombre_alumno = ctk.CTkLabel(self.vista_alumno, text=f"{datos_alumno[1]} {datos_alumno[2]}")
            self.label_nombre_alumno.pack(pady=5)

            # Definir las columnas de la tabla
            columnas_va = ("ID", "Materia", "Tipo de inscripcion", "Dia limite para pagar cada mes", "Deuda", "Estado")

            self.frame_inscripciones_alumno = ctk.CTkFrame(self.vista_alumno)
            self.frame_inscripciones_alumno.pack(fill="both", expand=True)

            # Crear la tabla
            self.tabla_inscripciones_alumno = ttk.Treeview(self.frame_inscripciones_alumno, columns=columnas_va, show="headings", selectmode="browse")
            for col in columnas_va:
                self.tabla_inscripciones_alumno.heading(col, text=col)

            self.tabla_inscripciones_alumno.column("ID", width=0, stretch=False)

            self.tabla_inscripciones_alumno.bind("<<TreeviewSelect>>", self.on_tree_select_incripcion_alumno) # accion al seleccionar un registro

            self.tabla_inscripciones_alumno.pack(fill="both", expand=True)
            self.tabla_inscripciones_alumno.tag_configure('deudor', background='red')

            # Obtener datos de inscripciones del alumno
            self.cargar_inscripcion_alumno(alumno_id)

            # Crear frame para los botones debajo de la tabla
            self.buttons_frame_inscripciones_alumno = ctk.CTkFrame(self.frame_inscripciones_alumno, fg_color="transparent")
            self.buttons_frame_inscripciones_alumno.pack(padx=10, pady=10)

            # Crear botón "Editar inscripcion"
            self.btn_editar_inscripcion_alumno = ctk.CTkButton(self.buttons_frame_inscripciones_alumno, text="Editar Inscripción", command= self.editar_inscripcion_alumno ,state="disabled")
            self.btn_editar_inscripcion_alumno.grid(row=0, column=1, padx=5)

            # Crear botón "Editar inscripcion"
            self.btn_perdonar_deuda_alumno = ctk.CTkButton(self.buttons_frame_inscripciones_alumno, text="Perdonar deuda", command= lambda: self.perdonar_deuda_alumno(datos_alumno[1], datos_alumno[2]) ,state="disabled")
            self.btn_perdonar_deuda_alumno.grid(row=0, column=2, padx=5)

    def filtrar_por_alumno(self, alumno):
        # Limpiar tabla existente
        for item in self.tabla_alumno.get_children():
            self.tabla_alumno.delete(item)

        alumno_id = alumno.split(" - ")[0]

        alumno = get_unico_alumno(alumno_id)
        if alumno:
            if alumno[8] == "Si":
                self.tabla_alumno.insert("", tk.END, values=(alumno[0], alumno[1], alumno[2], alumno[3], alumno[4], alumno[5], alumno[6], alumno[7]), tags='deudor')
            else:
                self.tabla_alumno.insert("", tk.END, values=(alumno[0], alumno[1], alumno[2], alumno[3], alumno[4], alumno[5], alumno[6], alumno[7]))


    def actualizar_combobox(self, alumnos):
        # Filtra la lista de alumnos por el filtro (ignora mayúsculas/minúsculas)
        alumnos = [f"{alumno[0]} - {alumno[1]} {alumno[2]}"
                             for alumno in alumnos]
        self.optionmenu_alumno.configure(values=alumnos)

    def filtrar_alumnos(self, event):
        filtro = self.optionmenu_alumno.get()
        alumnos = get_alumnos_filtrados(filtro.lower())
        self.actualizar_combobox(alumnos)

    def editar_alumno(self):
        # Obtener el item seleccionado
        selected_item = self.tabla_alumno.selection()[0]
        if selected_item:
            alumno_data = self.tabla_alumno.item(selected_item, "values")
            threading.Thread(target=self.ventana_editar_alumno, args=(alumno_data, selected_item), daemon=True).start()

    def ventana_editar_alumno(self, alumno_data, selected_item):
        self.edit_window_alumno_frame = Toplevel(self)
        self.edit_window_alumno_frame.title("Editar Alumno")
        self.edit_window_alumno_frame.geometry("400x600")
        self.edit_window_alumno = ctk.CTkScrollableFrame(self.edit_window_alumno_frame)
        self.edit_window_alumno.pack(fill="both", expand=True)

        self.edit_window_alumno_frame.transient()
        self.edit_window_alumno_frame.grab_set()

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

    def filtrar_alumnos_por_materia(self, event):
        self.pagina_actual = 1
        self.cargar_alumnos()

    def guardar_cambios_alumno(self, selected_item, nombre, apellido, dni, calle, numero, email, telefono, paga_el, alumno_data):
        editado = editar_alumno(alumno_data[0], nombre, apellido, dni, calle, numero, email, telefono)
        editar_dia_de_pago_alumno(alumno_data[0], paga_el)
        if editado:
            # Actualizar el registro en la tabla con los nuevos datos
            self.tabla_alumno.item(selected_item, values=(alumno_data[0], nombre, apellido, dni, calle, numero, email, telefono))
            self.edit_window_alumno_frame.destroy()
            messagebox.showinfo(
                title="Exito",
                message="Alumno editado correctamente"
            )

    def cargar_inscripcion_alumno(self, id_alumno):
        
        # Limpiar tabla existente
        for item in self.tabla_inscripciones_alumno.get_children():
            self.tabla_inscripciones_alumno.delete(item)

        inscripciones_alumno = get_inscripciones_alumno(id_alumno)

        for inscripcion in inscripciones_alumno:
            deuda = inscripcion[4] - inscripcion[5]
            if inscripcion[7] == 'No':
                self.tabla_inscripciones_alumno.insert("", tk.END, values=(inscripcion[0],inscripcion[1],inscripcion[2],inscripcion[3],deuda,inscripcion[6]))
            elif inscripcion[7] == 'Si':
                self.tabla_inscripciones_alumno.insert("", tk.END, values=(inscripcion[0],inscripcion[1],inscripcion[2],inscripcion[3],deuda,inscripcion[6]), tags="deudor")

    def on_tree_select_incripcion_alumno(self, event):
        self.btn_editar_inscripcion_alumno.configure(state="normal")
        self.btn_perdonar_deuda_alumno.configure(state="normal")

    def editar_inscripcion_alumno(self):
        # Obtener el item seleccionado
        selected_item = self.tabla_inscripciones_alumno.selection()[0]
        if selected_item:
            inscripcion_alumno_data = self.tabla_inscripciones_alumno.item(selected_item, "values")
            self.ventana_editar_inscripcion_alumno(inscripcion_alumno_data, selected_item)

    def perdonar_deuda_alumno(self, nombre, apellido):
        # Obtener el item seleccionado
        selected_item = self.tabla_inscripciones_alumno.selection()[0]
        if selected_item:
            inscripcion_alumno_data = self.tabla_inscripciones_alumno.item(selected_item, "values")
            inscripcion_id = inscripcion_alumno_data[0]
            self.ventana_perdonar_deuda_alumno(nombre, apellido, inscripcion_id)
    
    def ventana_perdonar_deuda_alumno(self, nombre, apellido, id_inscripcion):
        nombre_alumno = nombre + ' ' + apellido  # Ajustá el índice según tu estructura de datos

        respuesta = messagebox.askyesno(
            "Confirmar acción",
            f"¿Estás seguro de que querés perdonar la deuda del alumno {nombre_alumno}?"
        )

        if respuesta:
            # Lógica para perdonar la deuda
            exito = perdonar_deuda_inscripcion(id_inscripcion)
            if exito:
                messagebox.showinfo("Éxito", f"La deuda del alumno {nombre_alumno} ha sido perdonada.")
            else:
                messagebox.showerror("Error", f"No se pudo sanear la deuda de {nombre_alumno}")
        else:
            messagebox.showinfo("Cancelado", "La acción fue cancelada.")
        

    def ventana_editar_inscripcion_alumno(self, inscripcion_data, selected_item):
        # Crear una nueva ventana para editar
        self.edit_window_inscripcion = Toplevel(self)
        self.edit_window_inscripcion.title("Editar Inscripciones de Alumno")
        self.edit_window_inscripcion.geometry("400x300")

        self.edit_window_inscripcion.transient()
        self.edit_window_inscripcion.grab_set()

        # Tipo Inscripcion
        label_tipo_inscripcion = ctk.CTkLabel(self.edit_window_inscripcion, text="Tipo Inscripción:")
        label_tipo_inscripcion.pack(pady=5)
        tipo_inscripcion_var = ctk.StringVar()
        tipo_inscripcion_var.set(inscripcion_data[2])

        # obtenemos los valores para el dropdown de inscripciones
        tipo_inscripciones = self.get_tipo_inscripciones()
        lista_tipo_inscripciones = [f"{inscripcion[1]}" for inscripcion in tipo_inscripciones]

        self.combobox_inscripcion = ctk.CTkComboBox(self.edit_window_inscripcion,
                                                    variable=tipo_inscripcion_var,
                                                    values=lista_tipo_inscripciones,
                                                    width=300,
                                                    )
        self.combobox_inscripcion.pack(pady=5)

        # Estado Inscripcion
        label_estado_inscripcion = ctk.CTkLabel(self.edit_window_inscripcion, text="Estado de Inscripción:")
        label_estado_inscripcion.pack(pady=5)
        estado_inscripcion_var = ctk.StringVar()
        estado_inscripcion_var.set(inscripcion_data[5])

        self.combobox_estado_inscripcion = ctk.CTkComboBox(self.edit_window_inscripcion,
                                                    variable=estado_inscripcion_var,
                                                    values=['curso','finalizado','baja'],
                                                    width=300,
                                                    )
        self.combobox_estado_inscripcion.pack(pady=5)

        # Dia limite de pago
        label_paga_el_incripcion = ctk.CTkLabel(self.edit_window_inscripcion, text="Dia limite de pago cada mes")
        label_paga_el_incripcion.pack(pady=5)
        entry_paga_el_incripcion = ctk.CTkEntry(self.edit_window_inscripcion)
        entry_paga_el_incripcion.pack(pady=5)
        entry_paga_el_incripcion.insert(0, inscripcion_data[3])

        # Botón para guardar los cambios
        btn_guardar_inscripcion = ctk.CTkButton(self.edit_window_inscripcion,
                                                text="Guardar",
                                                command=lambda: self.guardar_cambios_inscripcion(
                                                        selected_item,
                                                        tipo_inscripcion_var.get(),
                                                        entry_paga_el_incripcion.get(),
                                                        estado_inscripcion_var.get(),
                                                        inscripcion_data))
        btn_guardar_inscripcion.pack(pady=10)

    def guardar_cambios_inscripcion(self, selected_item, tipo, paga_el, estado, inscripcion_data):
        editado = editar_inscripcion(inscripcion_data[0], tipo, paga_el, estado)
        if editado:
            # Actualizar el registro en la tabla con los nuevos datos
            self.tabla_inscripciones_alumno.item(selected_item, values=(inscripcion_data[0], inscripcion_data[1], tipo, paga_el, inscripcion_data[4], estado))
            messagebox.showinfo(
                title="Exito",
                message="Inscripción de alumno editada correctamente"
            )
            self.edit_window_inscripcion.destroy()

    def get_tipo_inscripciones(self):
        inscripciones = get_descripciones()
        return inscripciones