import customtkinter as ctk
from typing import Callable

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, navigation_callback: Callable, user_role: str):
        super().__init__(parent, width=200)
        self.navigation_callback = navigation_callback
        self.user_role = user_role
        self.setup_sidebar()
        
    def setup_sidebar(self):
        self.pack(side="left", fill="y", ipadx=6)
        self.create_navigation_buttons()
    
    def create_navigation_buttons(self):
        # Definir los botones y sus propiedades
        buttons = self.get_buttons_config()
        
        for btn_config in buttons:
            if btn_config.get("role") and btn_config["role"] != self.user_role:
                continue
                
            btn = ctk.CTkButton(
                self,
                text=btn_config["text"],
                width=100,
                command=lambda page=btn_config["page"]: 
                    self.navigation_callback(page)
            )
            btn.pack(pady=10, anchor='center')
    
    def get_buttons_config(self) -> list:
        return [
            {"text": "Alta Alumno", "page": "alta_alumno"},
            {"text": "Alta Gasto", "page": "alta_gasto"},
            {"text": "Alta Pago", "page": "alta_pago"},
            {"text": "Alta Inscripción", "page": "alta_inscripcion"},
            {"text": "Ver Pagos", "page": "ver_pagos"},
            {"text": "Ver Gastos", "page": "ver_gastos", "role": "administrador"},
            {"text": "Ver Movimientos", "page": "ver_movimientos"},
            {"text": "Ver Alumnos", "page": "ver_alumnos"},
            {"text": "Ajustes", "page": "ajustes"}
        ]