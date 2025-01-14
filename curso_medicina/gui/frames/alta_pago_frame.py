from curso_medicina.database.operations.alumno_operations import get_alumnos, get_cuotas_por_alumno_materia
from curso_medicina.database.operations.materia_operations import get_materias, get_materias_por_alumno
from curso_medicina.database.operations.pagos_operations import insert_pago, get_info_ultimo_pago, insert_pago_moneda_extranjera
from curso_medicina.database.operations.inscripcion_operations import finalizar_inscripcion, get_inscripcion_alumno_materia, get_info_inscripcion
from curso_medicina.database.operations.deuda_operations import sanear_deuda
from ..utils.receipt_generator import generate_payment_receipt
from ..utils.validators import is_valid_date

from tkinter import messagebox, simpledialog
from datetime import datetime
import os

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

        # Materia
        self.label_materia = ctk.CTkLabel(self, text="Materia:")
        self.label_materia.pack(pady=5)
        self.materia_var = ctk.StringVar()
        self.combobox_materia = ctk.CTkOptionMenu(self, variable=self.materia_var, values=self.materias, width=300, command=self.actualizar_cuotas)
        self.combobox_materia.pack(pady=5)

        # Mostrar la informacion del tipo de inscripcion
        self.label_info_inscripcion = ctk.CTkLabel(self, text="", text_color="#0066ff")
        self.label_info_inscripcion.pack(pady=3)
        
        # Label y Entry para monto
        self.label_monto = ctk.CTkLabel(self, text="Monto:")
        self.label_monto.pack(pady=5)
        self.entry_monto = ctk.CTkEntry(self, width=300)
        self.entry_monto.pack(pady=5)

        # Label y Entry para divisa
        self.label_divisa = ctk.CTkLabel(self, text="Divisa:")
        self.label_divisa.pack(pady=5)
        self.divisa_var = ctk.StringVar()
        self.divisa_var.set("Peso")
        self.entry_divisa = ctk.CTkOptionMenu(self, variable=self.divisa_var,values=['Peso','Real','Dolar'],width=300)
        self.entry_divisa.pack(pady=5)

        # Label y Entry para fecha
        self.label_fecha = ctk.CTkLabel(self, text="Fecha (AAAA-MM-DD):")
        self.label_fecha.pack(pady=5)
        self.fecha_var = ctk.StringVar()
        self.entry_fecha = ctk.CTkEntry(self, textvariable=self.fecha_var, width=300)
        self.entry_fecha.pack(pady=5)

        hoy = datetime.now().strftime("%Y-%m-%d")
        self.fecha_var.set(hoy)

        # Label y Entry para metodo de pago
        self.label_metodo = ctk.CTkLabel(self, text="Método de Pago")
        self.label_metodo.pack(pady=5)
        self.metodo_var = ctk.StringVar()
        self.entry_metodo = ctk.CTkOptionMenu(self,
                                              variable=self.metodo_var,values=['Efectivo','Transferencia'],
                                              command=self.on_metodo_seleccionado,
                                              width=300)
        self.entry_metodo.pack(pady=5)
        
        # Label y Entry para cuota
        self.label_cuota = ctk.CTkLabel(self, text="Cuota número:")
        self.label_cuota.pack(pady=5)
        self.cuota_var = ctk.StringVar()
        self.combobox_cuota = ctk.CTkComboBox(self, variable=self.cuota_var,values=[],width=300)
        self.combobox_cuota.pack(pady=5)

        # Label y Entry para correspondencia
        self.label_correspondencia = ctk.CTkLabel(self, text="Cuenta:")
        self.label_correspondencia.pack(pady=5)
        self.correspondencia_var = ctk.StringVar()
        self.entry_correspondencia = ctk.CTkOptionMenu(self,
                                                       variable=self.correspondencia_var,
                                                       values=["enyn", "Fernanda", "Felipe", "Duanne", "Flávia"],
                                                       width=300)
        self.entry_correspondencia.pack(pady=5)

        # Label y Entry para observacion
        self.label_descripcion = ctk.CTkLabel(self, text="Observaciones")
        self.label_descripcion.pack(pady = 5)
        self.entry_descripcion = ctk.CTkTextbox(self, width=300, height=50)
        self.entry_descripcion.pack(pady = 5)

    def create_save_button(self):
        # Botón para guardar el pago
        btn_guardar = ctk.CTkButton(self, text="Guardar Pago", width=150,
                                    command=lambda: self.save_pago(self.alumno_var.get(),
                                                                      self.materia_var.get(),
                                                                      self.entry_monto.get(),
                                                                      self.divisa_var.get(),
                                                                      self.metodo_var.get(),
                                                                      self.cuota_var.get(),
                                                                      self.correspondencia_var.get(),
                                                                      self.fecha_var.get(),
                                                                      self))
        btn_guardar.pack(pady=20)

    def actualizar_combobox(self, filtro):
        # Filtra la lista de alumnos por el filtro (ignora mayúsculas/minúsculas)
        alumnos_filtrados = [f"{alumno[0]} - {alumno[1]} {alumno[2]}" for alumno in self.alumnos if alumno[1].lower().startswith(filtro.lower())]
        self.combobox_alumno.configure(values=alumnos_filtrados)

    def filtrar_alumnos(self, event):
        filtro = self.combobox_alumno.get()
        self.actualizar_combobox(filtro)
    
    def save_pago(self, alumno_seleccionado, materia, monto, divisa, metodo, cuota, correspondencia, fecha, ventana):
        if alumno_seleccionado and materia and monto and divisa and cuota:
            if metodo == "Transferencia" and correspondencia == "":
                messagebox.showerror("Advertencia", "Debe elegir la cuenta para pagos realizados por transferencia")
            elif metodo == "Efectivo" and correspondencia != "":
                messagebox.showerror("Advertencia", "Para pagos en efectivo debe seleccionar 'No aplica' en el campo de cuenta")
            else:
                try:
                    alumno_id = int(alumno_seleccionado.split(" - ")[0])
                    materia_id = int(materia.split(" - ")[0])
                    monto = float(monto)

                    if not is_valid_date(fecha):
                        messagebox.showerror("Error", "Debe proporcionar una fecha valida con el formato correcto (AAAA-MM-DD)")
                        return

                    if divisa == "Real" or divisa == "Dolar": #caso moneda extranjera
                        monto_en_pesos = self.ask_exchange_rate(divisa)
                        pago_id = insert_pago(self.conn, alumno_id, materia_id, monto_en_pesos, divisa, metodo, cuota, correspondencia, fecha, self.entry_descripcion.get("1.0", "end-1c"), self.usuario_actual.id)
                        # guardamos ademas el registro en moneda extranjera
                        insert_pago_moneda_extranjera(self.conn, pago_id, divisa, monto)

                    elif divisa == "Peso":   #caso moneda local
                        pago_id = insert_pago(self.conn, alumno_id, materia_id, monto, divisa, metodo, cuota, correspondencia, fecha, self.entry_descripcion.get("1.0", "end-1c"),self.usuario_actual.id)

                    else: messagebox.showerror("Error", "Seleccione una divisa de la lista")

                    if pago_id:
                        messagebox.showinfo("Éxito", f"Pago ID {pago_id} guardado correctamente")
                        self.chequear_deuda(pago_id, cuota)
                        cuotas_restantes = self.combobox_cuota.cget("values")
                        if len(cuotas_restantes) <= 1:
                            self.chequear_fin_inscripcion(pago_id, cuota)
                        self.clear_fields()
                        self.generate_receipt(pago_id, alumno_seleccionado, materia, monto, divisa, metodo, cuota, correspondencia)
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
        try:
            alumno_id = int(alumno_seleccionado.split(" - ")[0])
        except ValueError:
            self.combobox_materia.configure(values=self.materias)
            self.label_info_inscripcion.configure(text="")
            return
        materia_id = int(materia_seleccionada.split(" - ")[0])
        inscripcion_alumno_materia = get_inscripcion_alumno_materia(self.conn, alumno_id, materia_id)
        n_cuotas = inscripcion_alumno_materia[-1]
        if alumno_seleccionado and materia_seleccionada:
            cuotas = get_cuotas_por_alumno_materia(self.conn, alumno_id, materia_id)
            valores_cuotas = [f"{i}" for i in range(cuotas[-1] + 1, n_cuotas + 1)]
            self.combobox_cuota.configure(values=valores_cuotas)
            self.display_info_inscripcion(inscripcion_alumno_materia[0])

    def chequear_fin_inscripcion(self, pago_id, cuota):
        info_pago = get_info_ultimo_pago(self.conn, pago_id, cuota)
        monto_pagado = sum([pago[2] for pago in info_pago])
        deuda = info_pago[-1][-1]
        id_inscripcion = info_pago[0][1]
        if monto_pagado >= deuda:
            finalizar_inscripcion(self.conn, id_inscripcion)
            messagebox.showinfo(
                title="Pago de curso completado",
                message="El alumno terminó de pagar todas las cuotas para esta materia"
            )

    def chequear_deuda(self, pago_id, cuota):
        info_pago = get_info_ultimo_pago(self.conn, pago_id, cuota)
        monto_pagado = sum([pago[2] for pago in info_pago])
        deuda = info_pago[-1][-1]
        id_inscripcion = info_pago[0][1]
        if monto_pagado >= deuda:
            sanear_deuda(self.conn, id_inscripcion, cuota)

    def on_metodo_seleccionado(self, event):
        if self.metodo_var.get() == "Transferencia":
            self.entry_correspondencia.configure(state="normal")
        else:
            self.correspondencia_var.set("")
            self.entry_correspondencia.configure(state="disabled")

    def display_info_inscripcion(self, id_inscripcion):
        info_inscripcion = get_info_inscripcion(self.conn, id_inscripcion)
        self.label_info_inscripcion.configure(text=f"Inscripción {info_inscripcion[3]}: {info_inscripcion[2]} cuotas de {info_inscripcion[0]} o {info_inscripcion[1]} con recargo")

    def generate_receipt(self, pago_id, alumno_seleccionado, materia, monto, divisa, metodo, cuota, correspondencia):
        try:
            
            # Generar el reporte
            output_path = generate_payment_receipt(pago_id, alumno_seleccionado, materia, monto, divisa, metodo, cuota, correspondencia)

            # Verificar si el usuario seleccionó una ubicación
            if not output_path:
                return None  # El usuario canceló la selección
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Éxito", 
                f"Reporte generado exitosamente en:\n{output_path}"
            )
            
            # Abrir el archivo con el visor de PDF predeterminado
            os.startfile(output_path) if os.name == 'nt' else os.system(f'xdg-open "{output_path}"')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {str(e)}")

    @staticmethod
    def ask_exchange_rate(divisa):
        """
        Solicita al usuario la tasa de cambio para la divisa seleccionada
        """
        rate = simpledialog.askfloat(
            "Total en pesos",
            f"Ingrese el equivalente en pesos del pago en {divisa}es:",
            minvalue=0.01
        )
        return rate
        

    def clear_fields(self):
        self.alumno_var.set("")
        self.materia_var.set("")
        self.entry_monto.delete(0, "end")
        self.divisa_var.set("")
        self.correspondencia_var.set("")
        self.cuota_var.set("")
        self.entry_descripcion.delete("1.0", "end-1c")
        self.fecha_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.metodo_var.set("")