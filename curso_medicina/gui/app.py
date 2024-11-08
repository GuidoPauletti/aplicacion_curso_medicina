import customtkinter as ctk
from curso_medicina.gui.frames.login_frame import LoginFrame, UserData
from curso_medicina.gui.frames.sidebar import Sidebar
from curso_medicina.gui.frames.alta_alumno_frame import AltaAlumnoFrame
from curso_medicina.gui.frames.alta_gasto_frame import AltaGastoFrame
from curso_medicina.gui.frames.alta_pago_frame import AltaPagoFrame
from curso_medicina.gui.frames.ver_pagos_frame import VerPagosFrame


class Aplicacion:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.setup_main_window()
        self.show_login()
        
    def setup_main_window(self):
        self.root.title("Sistema de Gestión de Cursos de Medicina")
        self.root.geometry("800x600")
        
    def show_login(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Mostrar frame de login
        LoginFrame(self.root, self.conn, self.on_login_success)
        
    def on_login_success(self, user: UserData):
        self.usuario_actual = user
        self.show_main_page()
        
    def show_main_page(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Configurar navegación principal
        self.setup_navigation()
        
    def setup_navigation(self):
        # Crear sidebar
        self.sidebar = Sidebar(
            self.root,
            navigation_callback=self.navigate_to,
            user_role=self.usuario_actual.rol
        )
        
        # Crear frame principal para contenido
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Iniciar con la página predeterminada
        self.navigate_to("alta_alumno")
    
    def navigate_to(self, page: str):
        # Limpiar el frame de contenido actual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Diccionario de frames disponibles
        frames = {
            "alta_alumno": lambda: AltaAlumnoFrame(self.content_frame, self.conn),
            "alta_gasto": lambda: AltaGastoFrame(self.content_frame, self.conn, self.usuario_actual),
            "alta_pago": lambda: AltaPagoFrame(self.content_frame, self.conn, self.usuario_actual),
            "ver_pagos": lambda: VerPagosFrame(self.content_frame, self.conn)
        }
        
        # Crear y mostrar el frame correspondiente
        if page in frames:
            frame = frames[page]()
            frame.pack(fill="both", expand=True)