from curso_medicina.database.connection import get_connection

from typing import Optional, Tuple
from tkinter import messagebox

import mysql.connector
from mysql.connector.cursor import MySQLCursor

def validate_user_credentials(
    nombre: str,
    apellido: str,
    password: str
) -> Optional[Tuple]:
    try:
        connection = get_connection()
        cursor: MySQLCursor = connection.cursor()
        
        sql_query = """
        SELECT id, nombre, apellido, contraseña, privilegio
        FROM usuario
        WHERE nombre = %s AND apellido = %s AND contraseña = %s
        """
        
        cursor.execute(sql_query, (nombre, apellido, password))
        result = cursor.fetchone()
        
        return result
        
    except mysql.connector.Error as error:
        messagebox.showerror(
            title="Error",
            message=f"Error al validar credenciales: {error}"
        )
        return None
    finally:
        cursor.close()
        connection.close()