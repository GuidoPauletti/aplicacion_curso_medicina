from tkinter import messagebox

import mysql.connector
from mysql.connector import Error

def create_connection():
    """Crear una conexión a la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(
            host="149.50.133.127",
            user="miscellium",
            password="M&sc3LLium$",
            database="curso_medicina",
            port=3306
        )
        return connection

    except Error as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al conectar a MySQL: {e}"
        )
        return None