from curso_medicina.database.operations.auth_operations import validate_user_credentials
from curso_medicina.gui.utils.validators import validate_login_input

from dataclasses import dataclass
from typing import Callable, Optional
from tkinter import messagebox

import customtkinter as ctk


@dataclass
class UserData:
    id: int
    nombre: str
    apellido: str
    rol: str

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, conn, on_login_success: Callable[[UserData], None]):
        super().__init__(parent, fg_color="transparent")
        self.conn = conn
        self.on_login_success = on_login_success
        self.error_label: Optional[ctk.CTkLabel] = None
        self.setup_ui()
        
    def setup_ui(self):
        self.pack(pady=50, padx=50)
        self.create_login_form()
        
    def create_login_form(self):
        # Campos de entrada
        self.nombre_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nombre",
            width=200
        )
        self.nombre_entry.pack(pady=10)
        
        self.apellido_entry = ctk.CTkEntry(
            self,
            placeholder_text="Apellido",
            width=200
        )
        self.apellido_entry.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Contraseña",
            show="*",
            width=200
        )
        self.password_entry.pack(pady=10)
        
        # Botón de login
        self.login_button = ctk.CTkButton(
            self,
            text="Iniciar sesión",
            command=self.handle_login,
            width=200
        )
        self.login_button.pack(pady=20)
        
    def handle_login(self):
        # Obtener datos del formulario
        credentials = {
            'nombre': self.nombre_entry.get(),
            'apellido': self.apellido_entry.get(),
            'password': self.password_entry.get()
        }
        
        # Validar entrada
        if not validate_login_input(credentials):
            self.show_error("Por favor complete todos los campos")
            return
            
        # Validar credenciales
        user_data = validate_user_credentials(self.conn, **credentials)
        
        if user_data:
            # Crear objeto UserData
            user = UserData(
                id=user_data[0],
                nombre=user_data[1],
                apellido=user_data[2],
                rol=user_data[4]
            )
            self.on_login_success(user)
        else:
            self.show_error("Usuario o contraseña incorrectos")
    
    def show_error(self, message: str):
        if self.error_label:
            self.error_label.configure(text=message)
        else:
            self.error_label = ctk.CTkLabel(
                self,
                text=message,
                text_color="red"
            )
            self.error_label.pack(pady=10)