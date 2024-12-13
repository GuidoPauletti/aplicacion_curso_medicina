import customtkinter as ctk
from typing import Callable

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, navigation_callback: Callable, user_role: str):
        super().__init__(parent, width=200)
        self.navigation_callback = navigation_callback
        self.user_role = user_role
        self.currently_selected_btn = None
        self.setup_sidebar()
        
    def setup_sidebar(self):
        self.pack(side="left", fill="y", ipadx=6)
        self.create_navigation_buttons()
    
    def create_navigation_buttons(self):
        # Definir los botones y sus propiedades
                
        btn_alta_alumno = ctk.CTkButton(
            self,
            text="Alta Alumno",
            width=100,
            border_width=2,
            border_color="black"
        )
        btn_alta_alumno.configure(command = lambda: self.navigation("alta_alumno", btn_alta_alumno))
        btn_alta_alumno.pack(pady=10, anchor='center')
        
        self.currently_selected_btn = btn_alta_alumno

        btn_alta_gasto = ctk.CTkButton(
            self,
            text="Alta Gasto",
            width=100
        )
        btn_alta_gasto.configure(command = lambda: self.navigation("alta_gasto", btn_alta_gasto))
        btn_alta_gasto.pack(pady=10, anchor='center')

        btn_alta_pago = ctk.CTkButton(
            self,
            text="Alta Pago",
            width=100
        )
        btn_alta_pago.configure(command = lambda: self.navigation("alta_pago", btn_alta_pago))
        btn_alta_pago.pack(pady=10, anchor='center')

        btn_alta_inscripcion = ctk.CTkButton(
            self,
            text="Alta Inscripción",
            width=100
        )
        btn_alta_inscripcion.configure(command = lambda: self.navigation("alta_inscripcion", btn_alta_inscripcion))
        btn_alta_inscripcion.pack(pady=10, anchor='center')

        btn_ver_pagos = ctk.CTkButton(
            self,
            text="Ver Pagos",
            width=100
        )
        btn_ver_pagos.configure(command = lambda: self.navigation("ver_pagos", btn_ver_pagos))
        btn_ver_pagos.pack(pady=10, anchor='center')

        if self.user_role == "administrador":
            btn_ver_gastos = ctk.CTkButton(
                self,
                text="Ver Gastos",
                width=100
            )
            btn_ver_gastos.configure(command = lambda: self.navigation("ver_gastos", btn_ver_gastos))
            btn_ver_gastos.pack(pady=10, anchor='center')

        btn_ver_movimientos = ctk.CTkButton(
            self,
            text="Ver Movimientos",
            width=100
        )
        btn_ver_movimientos.configure(command = lambda: self.navigation("ver_movimientos", btn_ver_movimientos))
        btn_ver_movimientos.pack(pady=10, anchor='center')

        btn_ver_alumnos = ctk.CTkButton(
            self,
            text="Ver Alumnos",
            width=100
        )
        btn_ver_alumnos.configure(command = lambda: self.navigation("ver_alumnos", btn_ver_alumnos))
        btn_ver_alumnos.pack(pady=10, anchor='center')

        btn_ajustes = ctk.CTkButton(
            self,
            text="Ajustes",
            width=100
        )
        btn_ajustes.configure(command = lambda: self.navigation("ajustes", btn_ajustes))
        btn_ajustes.pack(pady=10, anchor='center')

    def navigation(self, page, button):
        # Cambiar el estilo del botón activo
        if self.currently_selected_btn:
            self.currently_selected_btn.configure(border_width=0)  # Resetear estilo del anterior

        # Aplicar estilo al nuevo botón activo
        button.configure(border_width=2, border_color="black")
        self.currently_selected_btn = button

        # Lógica de navegación (cambiar la ventana actual)
        self.navigation_callback(page)
