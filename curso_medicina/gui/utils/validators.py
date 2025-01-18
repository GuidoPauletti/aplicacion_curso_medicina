from tkinter import messagebox
from datetime import datetime

def validate_login_input(data: dict) -> bool:
    """Valida que todos los campos necesarios estén presentes y no vacíos."""
    required_fields = ['nombre', 'apellido', 'password']
    return all(data.get(field, '').strip() for field in required_fields)

def validate_alumno_input(data):
    required_fields = ['nombre', 'apellido', 'dni', 'email', 'telefono','dir_calle', 'dir_numero']
    if not all(data.get(field, '').strip() for field in required_fields):
        messagebox.showerror(
            "Error",
            "Todos los campos son obligatorios"
        )
        return False
    return True

def validate_gasto_input(data):
    required_fields = ["monto", "divisa", "metodo"]
    if not all(data.get(field, '').strip() for field in required_fields):
        messagebox.showerror(
            "Error",
            "Los campos monto, divisa y metodo son obligatorios"
        )
        return False
    return True

def is_valid_date(date_string):
    try:
        # Intentar convertir la cadena a un objeto datetime con el formato YYYY-MM-DD
        datetime.strptime(date_string, "%Y-%m-%d")
        return True  # Si no hay excepción, la fecha es válida
    except ValueError:
        return False  # Si hay excepción, la fecha es inválida