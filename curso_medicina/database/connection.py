import mysql.connector
from mysql.connector import Error

def create_connection():
    """Crear una conexión a la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(
            host="34.171.118.187",
            user="root",
            password="f/J+*)<1_'zTr09g",
            database="curso_medicina"
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
        return connection

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None