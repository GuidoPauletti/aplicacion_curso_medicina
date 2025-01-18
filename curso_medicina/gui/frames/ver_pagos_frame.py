from curso_medicina.database.operations.pagos_operations import get_pagos_con_detalles, borrar_pago, editar_pago
from curso_medicina.database.operations.alumno_operations import get_alumnos

from tkinter import ttk, messagebox

import customtkinter as ctk

class VerPagosFrame(ctk.CTkFrame):
    def __init__(self, parent, conn, usuario_actual):
        super().__init__(parent)
        self.conn = conn
        self.usuario_actual = usuario_actual
        self.setup_ui()

    def setup_ui(self):
        # Crear elementos de filtro
        self.frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtros.pack(pady=5)

        self.label_filtro_cuenta = ctk.CTkLabel(self.frame_filtros, text="Filtrar por Cuenta:")
        self.label_filtro_cuenta.grid(row=0, column=0, padx=5)

        self.label_filtro_alumno = ctk.CTkLabel(self.frame_filtros, text="Filtrar por Alumno:")
        self.label_filtro_alumno.grid(row=0, column=1, padx=5)
        
        self.optionmenu_correspondencia = ctk.CTkOptionMenu(
            self.frame_filtros,
            values=["Todos", "enyn", "Fernanda", "Felipe", "Duanne", "Flávia", "Gabriel"],
            command=self.filtrar_por_correspondencia
        )
        self.optionmenu_correspondencia.grid(row=1, column=0, padx=5)

        # Obtener lista de alumnos
        self.alumnos = get_alumnos(self.conn)

        self.alumno_var = ctk.StringVar()
        self.optionmenu_alumno = ctk.CTkComboBox(
            self.frame_filtros,
            variable=self.alumno_var,
            command=self.filtrar_por_alumno
        )
        self.optionmenu_alumno.grid(row=1, column=1, padx=5)

        self.actualizar_combobox("")  # Inicializa la lista completa

        # Evento para filtrar nombres mientras se escribe en el ComboBox
        self.optionmenu_alumno.bind('<KeyRelease>', self.filtrar_alumnos)

        # Crear tabla
        columnas = ("ID", "Nombre", "Apellido", "Materia", "Monto (AR$)", "Metodo", "Cuenta", "Cuota", "Fecha", "Responsable", "Observaciones")

        self.scrollable_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        self.scrollable_frame.pack(fill="both", expand=True)
        
        self.tabla = ttk.Treeview(self.scrollable_frame, columns=columnas, show="headings", selectmode="browse")
        
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

    def cargar_pagos(self, correspondencia="Todos", alumno = None):
        # Limpiar tabla existente
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        # Traer info de pagos desde base de datos
        pagos = get_pagos_con_detalles(self.conn, correspondencia, alumno)
        for pago in pagos:
            self.tabla.insert("", "end", values=pago)

    def filtrar_por_correspondencia(self, correspondencia):
        alumno = self.alumno_var.get()
        if alumno == "":
            self.cargar_pagos(correspondencia)
        else:
            self.cargar_pagos(correspondencia, alumno[0])

    def filtrar_por_alumno(self, alumno):
        self.cargar_pagos(self.optionmenu_correspondencia.get(), alumno[0])

    def actualizar_combobox(self, filtro):
        # Filtra la lista de alumnos por el filtro (ignora mayúsculas/minúsculas)
        alumnos_filtrados = [f"{alumno[0]} - {alumno[1]} {alumno[2]}"
                             for alumno in self.alumnos
                             if alumno[1].lower().startswith(filtro.lower())
                             or alumno[2].lower().startswith(filtro.lower())]
        self.optionmenu_alumno.configure(values=alumnos_filtrados)

    def filtrar_alumnos(self, event):
        filtro = self.optionmenu_alumno.get()
        self.actualizar_combobox(filtro)

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
        self.edit_window_pago.geometry("400x550")

        label_monto = ctk.CTkLabel(self.edit_window_pago, text="Monto")
        label_monto.pack(pady=5)
        entry_monto = ctk.CTkEntry(self.edit_window_pago)
        entry_monto.pack(pady=5)
        entry_monto.insert(0, pago_data[4])

        label_cuota = ctk.CTkLabel(self.edit_window_pago, text="Cuota")
        label_cuota.pack(pady=5)
        entry_cuota = ctk.CTkEntry(self.edit_window_pago)
        entry_cuota.pack(pady=5)
        entry_cuota.insert(0, pago_data[7])

        # Label y Entry para metodo de pago
        label_metodo = ctk.CTkLabel(self.edit_window_pago, text="Método de Pago")
        label_metodo.pack(pady=5)
        metodo_var = ctk.StringVar()
        entry_metodo = ctk.CTkOptionMenu(self.edit_window_pago,
                                              variable=metodo_var,values=['Efectivo','Transferencia'],
                                              width=300)
        entry_metodo.pack(pady=5)
        metodo_var.set(pago_data[5])

        # Label y Entry para correspondencia
        label_correspondencia = ctk.CTkLabel(self.edit_window_pago, text="Cuenta:")
        label_correspondencia.pack(pady=5)
        correspondencia_var = ctk.StringVar()
        entry_correspondencia = ctk.CTkOptionMenu(self.edit_window_pago,
                                                       variable=correspondencia_var,
                                                       values=["enyn", "Fernanda", "Felipe", "Duanne", "Flávia", "Gabriel"],
                                                       width=300)
        entry_correspondencia.pack(pady=5)
        correspondencia_var.set(pago_data[6])

        # Botón para guardar los cambios
        btn_guardar = ctk.CTkButton(self.edit_window_pago, text="Guardar",
                                    command=lambda:self.guardar_cambios_pago(selected_item,
                                                                             entry_monto.get(),
                                                                             entry_cuota.get(),
                                                                             metodo_var.get(),
                                                                             correspondencia_var.get(),
                                                                             pago_data))
        btn_guardar.pack(pady=10)

    def guardar_cambios_pago(self, selected_item, monto, cuota, metodo, correspondencia, pago_data):
        editado = editar_pago(self.conn, pago_data[0], monto, cuota, metodo, correspondencia, self.usuario_actual.id)
        if editado:
            # Actualizar el registro en la tabla con los nuevos datos
            self.tabla.item(selected_item, values=(pago_data[0], pago_data[1], pago_data[2], pago_data[3], monto, metodo, correspondencia, cuota, pago_data[8], self.usuario_actual.nombre))
            messagebox.showinfo(
                title="Exito",
                message="Información de pago editada correctamente"
            )
            self.edit_window_pago.destroy()

    def on_tree_select(self, event):
        selected_items = self.tabla.selection()
        self.btn_borrar.configure(state="normal" if selected_items else "disabled")
        self.btn_editar.configure(state="normal" if selected_items else "disabled")

