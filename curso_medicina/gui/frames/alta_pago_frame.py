from curso_medicina.database.operations.alumno_operations import get_alumnos, get_cuotas_por_alumno_materia
from curso_medicina.database.operations.materia_operations import get_materias, get_materias_por_alumno
from curso_medicina.database.operations.pagos_operations import insert_pago

from tkinter import messagebox

import customtkinter as ctk


class AltaPagoFrame(ctk.CTkScrollableFrame):
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
        self.combobox_alumno = ctk.CTkComboBox(self, variable=self.alumno_var, width=300, command=self.actualizar_materias)

        self.combobox_alumno.pack(pady=5)
        self.actualizar_combobox("")  # Inicializa la lista completa

        # Evento para filtrar nombres mientras se escribe en el ComboBox
        self.combobox_alumno.bind('<KeyRelease>', self.filtrar_alumnos)

        # Obtener lista de materias
        self.materias = get_materias(self.conn)

        # Aquí va el código original de alta pago, adaptado para este frame.
        self.label_materia = ctk.CTkLabel(self, text="Materia:")
        self.label_materia.pack(pady=5)
        self.materia_var = ctk.StringVar()
        self.combobox_materia = ctk.CTkComboBox(self, variable=self.materia_var, values=self.materias, width=300, command=self.actualizar_cuotas)
        self.combobox_materia.pack(pady=5)
        
        # Label y Entry para monto
        self.label_monto = ctk.CTkLabel(self, text="Monto:")
        self.label_monto.pack(pady=5)
        self.entry_monto = ctk.CTkEntry(self, width=300)
        self.entry_monto.pack(pady=5)

        # Label y Entry para divisa
        self.label_divisa = ctk.CTkLabel(self, text="Divisa (Peso/Real):")
        self.label_divisa.pack(pady=5)
        self.divisa_var = ctk.StringVar()
        self.entry_divisa = ctk.CTkComboBox(self, variable=self.divisa_var,values=['Peso','Real','Dolar'],width=300)
        self.entry_divisa.pack(pady=5)

        # Label y Entry para efectivo
        self.label_efectivo = ctk.CTkLabel(self, text="Efectivo (Si/No):")
        self.label_efectivo.pack(pady=5)
        self.entry_efectivo = ctk.CTkEntry(self, width=300)
        self.entry_efectivo.pack(pady=5)
        
        # Label y Entry para cuota
        self.label_cuota = ctk.CTkLabel(self, text="Cuota número:")
        self.label_cuota.pack(pady=5)
        self.cuota_var = ctk.StringVar()
        self.combobox_cuota = ctk.CTkComboBox(self, variable=self.cuota_var,values=['Peso','Real','Dolar'],width=300)
        self.combobox_cuota.pack(pady=5)

        # Label y Entry para correspondencia
        self.label_correspondencia = ctk.CTkLabel(self, text="Corresponde a:")
        self.label_correspondencia.pack(pady=5)
        self.entry_correspondencia = ctk.CTkEntry(self, width=300)
        self.entry_correspondencia.pack(pady=5)

    def create_save_button(self):
        # Botón para guardar el pago
        btn_guardar = ctk.CTkButton(self, text="Guardar Pago", width=150,
                                    command=lambda: self.save_pago(self.alumno_var.get(),
                                                                      self.materia_var.get(),
                                                                      self.entry_monto.get(),
                                                                      self.divisa_var.get(),
                                                                      self.entry_efectivo.get(),
                                                                      self.cuota_var.get(),
                                                                      self.entry_correspondencia.get(),
                                                                      self.usuario_actual.id,
                                                                      self))
        btn_guardar.pack(pady=20)

    def actualizar_combobox(self, filtro):
        # Filtra la lista de alumnos por el filtro (ignora mayúsculas/minúsculas)
        alumnos_filtrados = [f"{alumno[0]} - {alumno[1]} {alumno[2]}" for alumno in self.alumnos if alumno[1].lower().startswith(filtro.lower())]
        self.combobox_alumno.configure(values=alumnos_filtrados)

    def filtrar_alumnos(self, event):
        filtro = self.combobox_alumno.get()
        self.actualizar_combobox(filtro)
    
    def save_pago(self, alumno_seleccionado, materia, monto, divisa, efectivo, cuota, correspondencia, usuario_actual, ventana):
        if alumno_seleccionado and materia and monto and divisa and cuota and correspondencia:
            try:
                alumno_id = int(alumno_seleccionado.split(" - ")[0])
                materia_id = int(materia.split(" - ")[0])
                if efectivo == 'Si': efectivo = 1
                else: efectivo = 0
                monto = float(monto)
                pago_id = insert_pago(self.conn, alumno_id, materia_id, monto, divisa, efectivo, cuota, correspondencia, self.usuario_actual.id)
                if pago_id:
                    messagebox.showinfo("Éxito", f"Pago ID {pago_id} guardado correctamente")
                    self.clear_fields()
                else:
                    messagebox.showerror("Error", "No se pudo guardar el pago")
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos. Verifique la información ingresada.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    def actualizar_materias(self, event):
        """Actualizar el combobox de materias según el alumno seleccionado."""
        alumno_seleccionado = self.combobox_alumno.get()
        if alumno_seleccionado:
            id_alumno = int(alumno_seleccionado.split(" - ")[0])  # Extraer el ID del alumno
            materias = get_materias_por_alumno(self.conn, id_alumno)
            materias_nombres = [f"{materia[0]} - {materia[1]}" for materia in materias]  # Obtenemos solo el nombre de las materias
            self.combobox_materia.configure(values=materias_nombres)

    def actualizar_cuotas(self, event):
        alumno_seleccionado = self.combobox_alumno.get()
        materia_seleccionada = self.combobox_materia.get()
        alumno_id = int(alumno_seleccionado.split(" - ")[0])
        materia_id = int(materia_seleccionada.split(" - ")[0])
        if alumno_seleccionado and materia_seleccionada:
            cuotas = get_cuotas_por_alumno_materia(self.conn, alumno_id, materia_id)
            valores_cuotas = [f"{i}" for i in range(cuotas[-1] + 1, 11)]
            self.combobox_cuota.configure(values=valores_cuotas)

    def clear_fields(self):
        self.alumno_var.set("")
        self.materia_var.set("")
        self.entry_monto.delete(0, "end")
        self.divisa_var.set("")
        self.entry_correspondencia.delete(0, "end")
        self.cuota_var.set("")
        self.entry_efectivo.delete(0, "end")