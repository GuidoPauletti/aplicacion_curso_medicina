from curso_medicina.database.operations.gasto_operations import get_gastos_con_detalles, borrar_gasto, editar_gasto

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from datetime import datetime

import customtkinter as ctk

class VerGastosFrame(ctk.CTkFrame):
    def __init__(self, parent, usuario_actual):
        super().__init__(parent)
        self.usuario_actual = usuario_actual
        self.setup_ui()

    def setup_ui(self):
        label_filtro = ctk.CTkLabel(self, text="Filtrar por Cuenta:")
        label_filtro.pack(pady=5)
        
        self.optionmenu_correspondencia_gasto = ctk.CTkOptionMenu(
            self, 
            values=["Todos", "enyn", "Fernanda", "Felipe", "Duanne", "Flávia", "Gabriel"],
            command=self.filtrar_por_correspondencia_gasto  # Asocia el filtro con el método
        )
        self.optionmenu_correspondencia_gasto.pack(pady=5)

        # Definir las columnas de la tabla
        columnas = ("ID","Monto", "Divisa", "Fecha", "Cuenta", "Metodo", "Descripcion", "Responsable")

        # Crear la tabla
        self.tabla_gasto = ttk.Treeview(self, columns=columnas, show="headings", selectmode="browse")
        # Configurar columnas
        for col in columnas:
            self.tabla_gasto.heading(col, text=col)

        self.tabla_gasto.column("ID", width=50, stretch=False)
        self.tabla_gasto.column("Monto", width=70)
        self.tabla_gasto.column("Fecha", width=70)

        self.tabla_gasto.bind("<<TreeviewSelect>>", self.on_tree_select_gasto) # accion al seleccionar un registro

        self.tabla_gasto.pack(fill="both", expand=True)

        # Obtener los pagos desde la base de datos
        self.cargar_gastos()

        # Crear frame para los botones debajo de la tabla
        self.buttons_frame_gasto = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame_gasto.pack(padx=10, pady=10)

        # Crear botón "Borrar registro"
        self.btn_borrar_gasto = ctk.CTkButton(self.buttons_frame_gasto, text="Borrar Registro", command=self.borrar_registro_gasto ,state="disabled")
        self.btn_borrar_gasto.grid(row=0, column=0, padx=5)

        # Crear botón "Editar registro"
        self.btn_editar_gasto = ctk.CTkButton(self.buttons_frame_gasto, text="Editar Registro", command=self.editar_registro_gasto,state="disabled")
        self.btn_editar_gasto.grid(row=0, column=1, padx=5)

    def on_tree_select_gasto(self, event):
        # Habilitar botones
        self.btn_borrar_gasto.configure(state="normal")
        self.btn_editar_gasto.configure(state="normal")

    def cargar_gastos(self, correspondencia="Todos"):
        # Obtener pagos de la base de datos
        gastos = get_gastos_con_detalles(correspondencia)  # Actualizamos la consulta con el filtro de correspondencia

        for gasto in gastos:
            self.tabla_gasto.insert("", tk.END, values=(gasto[0], gasto[1], gasto[2], gasto[3], gasto[4], gasto[5], gasto[6], gasto[7]))

    def filtrar_por_correspondencia_gasto(self, correspondencia):
        # Limpiar tabla
        for item in self.tabla_gasto.get_children():
            self.tabla_gasto.delete(item)

        self.cargar_gastos(correspondencia)

    def borrar_registro_gasto(self):
        # Obtener el item seleccionado
        selected_item = self.tabla_gasto.selection()[0]
        gasto_id = self.tabla_gasto.item(selected_item, "values")[0]
        if gasto_id:
            borrado = borrar_gasto(gasto_id)
            if borrado:
                self.tabla_gasto.delete(selected_item)

    def editar_registro_gasto(self):
        # Obtener el item seleccionado
        selected_item = self.tabla_gasto.selection()[0]
        if selected_item:
            gasto_data = self.tabla_gasto.item(selected_item, "values")
            self.ventana_editar_gasto(gasto_data, selected_item)

    def ventana_editar_gasto(self, gasto_data, selected_item):
        # Crear una nueva ventana para editar
        self.edit_window_gasto = Toplevel(self)
        self.edit_window_gasto.title("Editar Gasto")
        self.edit_window_gasto.geometry("400x550")

        self.edit_window_gasto.transient()
        self.edit_window_gasto.grab_set()

        label_monto = ctk.CTkLabel(self.edit_window_gasto, text="Monto")
        label_monto.pack(pady=5)
        entry_monto = ctk.CTkEntry(self.edit_window_gasto)
        entry_monto.pack(pady=5)
        entry_monto.insert(0, gasto_data[1])

        # Label y Entry para fecha
        label_fecha = ctk.CTkLabel(self.edit_window_gasto, text="Fecha (AAAA/MM/DD)")
        label_fecha.pack(pady=5)
        fecha_entry_var = ctk.StringVar()
        fecha_entry = ctk.CTkEntry(self.edit_window_gasto, textvariable = fecha_entry_var, placeholder_text="AAAA/MM/DD")
        fecha_entry.pack(pady=5)
        fecha_entry_var.set(gasto_data[3])

        # Label y Entry para correspondencia
        label_correspondencia = ctk.CTkLabel(self.edit_window_gasto, text="Cuenta:")
        label_correspondencia.pack(pady=5)
        correspondencia_var = ctk.StringVar()
        entry_correspondencia = ctk.CTkOptionMenu(self.edit_window_gasto,
                                                  variable=correspondencia_var,
                                                  values=["Todos", "enyn", "Fernanda", "Felipe", "Duanne", "Flávia", "Gabriel"],
                                                  width=300)
        entry_correspondencia.pack(pady=5)
        correspondencia_var.set(gasto_data[4])

        # Label y Entry para metodo de pago
        label_metodo = ctk.CTkLabel(self.edit_window_gasto, text="Método de Gasto")
        label_metodo.pack(pady=5)
        metodo_var = ctk.StringVar()
        entry_metodo = ctk.CTkOptionMenu(self.edit_window_gasto,
                                              variable=metodo_var,values=['Efectivo','Transferencia', 'Crédito', 'Debito'],
                                              width=300)
        entry_metodo.pack(pady=5)

        # Label y Entry para descripcion
        label_descripcion = ctk.CTkLabel(self.edit_window_gasto, text="Descripción")
        label_descripcion.pack(pady = 5)
        entry_descripcion = ctk.CTkTextbox(self.edit_window_gasto, width=300, height=200)
        entry_descripcion.pack(pady = 5)
        entry_descripcion.insert("1.0",gasto_data[6])

        # Botón para guardar los cambios
        btn_guardar = ctk.CTkButton(self.edit_window_gasto, text="Guardar", command=lambda: self.guardar_cambios_gasto(selected_item, entry_monto.get(), correspondencia_var.get(), metodo_var.get(), entry_descripcion.get("1.0", "end-1c"), gasto_data, fecha_entry_var.get()))
        btn_guardar.pack(pady=10)

    def guardar_cambios_gasto(self, selected_item, monto, correspondencia, metodo, descripcion, gasto_data, fecha):
        editado = editar_gasto(gasto_data[0], monto, correspondencia, metodo, descripcion, self.usuario_actual.id, fecha)
        if editado:
            # Actualizar el registro en la tabla con los nuevos datos
            self.tabla_gasto.item(selected_item, values=(gasto_data[0], monto, gasto_data[2], fecha, correspondencia, metodo, descripcion, self.usuario_actual.nombre))
            messagebox.showinfo(
                title="Exito",
                message="Gasto editado correctamente"
            )
            self.edit_window_gasto.destroy()