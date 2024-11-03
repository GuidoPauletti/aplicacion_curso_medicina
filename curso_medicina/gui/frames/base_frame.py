import customtkinter as ctk

class BaseFrame(ctk.CTkFrame):
    """
    Clase base para todos los frames de la aplicación.
    Proporciona funcionalidad común y estructura básica.
    """
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.conn = conn
        self.setup_ui()
    
    def setup_ui(self):
        """
        Método que debe ser implementado por las clases hijas
        para configurar su interfaz específica.
        """
        raise NotImplementedError("Debe implementar setup_ui en la clase hija")