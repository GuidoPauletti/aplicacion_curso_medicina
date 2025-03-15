from curso_medicina.database.operations.pagos_operations import get_pagos_con_detalles, borrar_pago, editar_pago
from curso_medicina.database.operations.alumno_operations import get_alumnos, get_alumnos_filtrados

from tkinter import ttk, messagebox
import threading
import queue

import customtkinter as ctk

class VerPagosFrame(ctk.CTkFrame):
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
        self.btn_actualizar = ctk.CTkButton(self.paginacion_frame, text="Actualizar", command=self.cargar_pagos)
        self.btn_actualizar.pack(side="right", padx=10)
        
        # Indicador de carga
        self.lbl_cargando = ctk.CTkLabel(self, text="")
        self.lbl_cargando.pack(pady=5)

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
        """Carga los datos de la página actual"""
        if self.loading:
            self.carga_cancelada = True
            self.lbl_cargando.configure(text="Cancelando carga anterior...")
            return
        
        self.carga_cancelada = False
        self.loading = True
        self.lbl_cargando.configure(text=f"Cargando datos...")

        # Limpiar tabla existente
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Deshabilitar controles durante la carga
        self.btn_anterior.configure(state="disabled")
        self.btn_siguiente.configure(state="disabled")
        self.btn_actualizar.configure(state="disabled")

        # Iniciar hilo de carga
        thread = threading.Thread(target=self.cargar_pagos_thread, args=(correspondencia, alumno), daemon=True)
        thread.start()


    def cargar_pagos_thread(self, correspondencia, alumno):
        try:
            pagos, total = get_pagos_con_detalles(correspondencia, alumno, self.pagina_actual, self.registros_por_pagina)

            if self.carga_cancelada:
                return
            
            # Actualizar información de paginación
            self.total_registros = total
            self.total_paginas = (total + self.registros_por_pagina - 1) // self.registros_por_pagina

            # Actualizar interfaz en el hilo principal
            self.after(0, lambda: self.mostrar_pagos(pagos))
            self.after(0, self.actualizar_controles_paginacion)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Error al cargar pagos: {e}"))
        
        finally:
            self.after(0, lambda: self.lbl_cargando.configure(text="Datos cargados"))
            self.after(0, lambda: setattr(self, 'loading', False))
            self.after(0, lambda: self.btn_actualizar.configure(state="normal"))

    def mostrar_pagos(self, pagos):
        for pago in pagos:
            self.tabla.insert("", "end", values=pago)

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
            alumno = self.alumno_var.get()
            if alumno == "":
                self.cargar_pagos(self.optionmenu_correspondencia.get())
            else:
                self.cargar_pagos(self.optionmenu_correspondencia.get(), alumno.split(" - ")[0])
    
    def pagina_siguiente(self):
        """Navega a la página siguiente"""
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            alumno = self.alumno_var.get()
            if alumno == "":
                self.cargar_pagos(self.optionmenu_correspondencia.get())
            else:
                self.cargar_pagos(self.optionmenu_correspondencia.get(), alumno.split(" - ")[0])

    def filtrar_por_correspondencia(self, correspondencia):
        self.pagina_actual = 1
        alumno = self.alumno_var.get()
        if alumno == "":
            self.cargar_pagos(correspondencia)
        else:
            self.cargar_pagos(correspondencia, alumno.split(" - ")[0])

    def filtrar_por_alumno(self, alumno):
        self.pagina_actual = 1
        self.cargar_pagos(self.optionmenu_correspondencia.get(), alumno.split(" - ")[0])

    def actualizar_combobox(self, alumnos):
        # Filtra la lista de alumnos por el filtro (ignora mayúsculas/minúsculas)
        alumnos = [f"{alumno[0]} - {alumno[1]} {alumno[2]}"
                             for alumno in alumnos]
        self.optionmenu_alumno.configure(values=alumnos)

    def filtrar_alumnos(self, event):
        filtro = self.optionmenu_alumno.get()
        alumnos = get_alumnos_filtrados(filtro.lower())
        self.actualizar_combobox(alumnos)

    def borrar_registro_pago(self):
        # Obtener el item seleccionado
        selected_item = self.tabla.selection()[0]
        pago_id = self.tabla.item(selected_item, "values")[0]
        if pago_id:
            borrado = borrar_pago(pago_id)
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
        editado = editar_pago(pago_data[0], monto, cuota, metodo, correspondencia, self.usuario_actual.id)
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

