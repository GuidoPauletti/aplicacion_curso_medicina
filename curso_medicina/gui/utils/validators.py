from tkinter import messagebox

def validate_login_input(data: dict) -> bool:
    """Valida que todos los campos necesarios estén presentes y no vacíos."""
    required_fields = ['nombre', 'apellido', 'password']
    return all(data.get(field, '').strip() for field in required_fields)

def validate_alumno_input(data):
    if not data['nombre'] or not data['apellido']:
        messagebox.showerror(
            "Error",
            "Nombre y apellido son campos obligatorios"
        )
        return False
    return True