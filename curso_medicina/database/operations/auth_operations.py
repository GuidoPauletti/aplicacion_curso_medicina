from typing import Optional, Tuple

import mysql.connector
from mysql.connector.cursor import MySQLCursor

def validate_user_credentials(
    connection: mysql.connector.MySQLConnection,
    nombre: str,
    apellido: str,
    password: str
) -> Optional[Tuple]:
    try:
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
        print(f"Error al validar credenciales: {error}")
        return None
    finally:
        cursor.close()