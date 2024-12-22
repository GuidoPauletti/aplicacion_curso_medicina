from curso_medicina.database.operations.inscripcion_operations import (get_info_inscripciones,
                                                                       editar_tipo_inscripcion,
                                                                       save_tipo_inscripcion)

from tkinter import messagebox
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
            command= self.ventana_crear_tipo_inscripcion
        )
        self.btn_crear.grid(row=0, column=0, padx=5)

        self.btn_editar = ctk.CTkButton(
            self.buttons_frame, 
            text="Editar Inscripción", 
            command=self.editar_tipo_inscripcion,
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

    def editar_tipo_inscripcion(self):
        # Obtener el item seleccionado
        selected_item = self.tabla.selection()[0]
        if selected_item:
            info_inscripcion = self.tabla.item(selected_item, "values")
            self.ventana_editar_pago(info_inscripcion, selected_item)

    def ventana_editar_pago(self, info_inscripcion, selected_item):
        # Crear una nueva ventana para editar
        self.edit_window_pago = ctk.CTkToplevel(self)
        self.edit_window_pago.title("Editar Tipo de Inscripción")
        self.edit_window_pago.geometry("500x500")

        label_descripcion = ctk.CTkLabel(self.edit_window_pago, text="Descripción")
        label_descripcion.pack(pady=5)
        entry_descripcion = ctk.CTkEntry(self.edit_window_pago)
        entry_descripcion.pack(pady=5)
        entry_descripcion.insert(0, info_inscripcion[1])

        label_monto = ctk.CTkLabel(self.edit_window_pago, text="Monto de cuota")
        label_monto.pack(pady=5)
        entry_monto = ctk.CTkEntry(self.edit_window_pago)
        entry_monto.pack(pady=5)
        entry_monto.insert(0, info_inscripcion[2])

        label_monto_recargo = ctk.CTkLabel(self.edit_window_pago, text="Monto de cuota con recargo")
        label_monto_recargo.pack(pady=5)
        entry_monto_recargo = ctk.CTkEntry(self.edit_window_pago)
        entry_monto_recargo.pack(pady=5)
        entry_monto_recargo.insert(0, info_inscripcion[3])

        label_n_cuotas = ctk.CTkLabel(self.edit_window_pago, text="Cantidad de cuotas")
        label_n_cuotas.pack(pady=5)
        entry_n_cuotas = ctk.CTkEntry(self.edit_window_pago)
        entry_n_cuotas.pack(pady=5)
        entry_n_cuotas.insert(0, info_inscripcion[4])

        # Botón para guardar los cambios
        btn_guardar = ctk.CTkButton(self.edit_window_pago,
                                    text="Guardar",
                                    command=lambda: self.guardar_cambios_inscripcion(selected_item,
                                                                              entry_descripcion.get(),
                                                                              entry_monto.get(),
                                                                              entry_monto_recargo.get(),
                                                                              entry_n_cuotas.get(),
                                                                              info_inscripcion))
        btn_guardar.pack(pady=10)

    def guardar_cambios_inscripcion(self, selected_item, descripcion, monto, monto_recargo, n_cuotas, info_inscripcion):
        editado = editar_tipo_inscripcion(self.conn, info_inscripcion[0], descripcion, monto, monto_recargo, n_cuotas)
        if editado:
            # Actualizar el registro en la tabla con los nuevos datos
            self.tabla.item(selected_item, values=(info_inscripcion[0], descripcion, monto, monto_recargo, n_cuotas))
            self.edit_window_pago.destroy()
            messagebox.showinfo(
                title="Tipo de inscripción editado correctamente",
                message=""
            )

    def ventana_crear_tipo_inscripcion(self):
        # Crear una nueva ventana para crear tipo de inscripcion
        self.create_window_inscripcion = ctk.CTkToplevel(self)
        self.create_window_inscripcion.title("Crear tipo de inscripción")
        self.create_window_inscripcion.geometry("500x500")

        label_descripcion = ctk.CTkLabel(self.create_window_inscripcion, text="Descripción")
        label_descripcion.pack(pady=5)
        entry_descripcion = ctk.CTkEntry(self.create_window_inscripcion, width=300, placeholder_text="Descripción breve del tipo de incripción")
        entry_descripcion.pack(pady=5)

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
            self.tabla.insert("", "end", values=(nuevo_tipo_incripcion, descripcion, cuota, cuota_recargo, n_cuotas))
            self.create_window_inscripcion.destroy()
            messagebox.showinfo(
                title="Exito",
                message="Tipo de inscripción creado correctamente"
            )
        else:
            return