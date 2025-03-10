from tkinter import messagebox
import threading
import time

import mysql.connector
from mysql.connector import Error

connection_pool = None
pool_lock = threading.Lock()


def init_connection_pool():
    """Crear una conexión a la base de datos MySQL"""
    global connection_pool

    with pool_lock:
        try:
            if connection_pool is None:
                connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="enyn_pool",
                    pool_size=5,
                    host="localhost",
                    user="root",
                    password="grootsql",
                    database="curso_medicina",
                    port=3306,
                    connection_timeout=10
                )
                print("Pool de conexiones inicializado correctamente")
            
                # Iniciar hilo de mantenimiento del pool
                maintenance_thread = threading.Thread(
                    target=_maintain_pool, 
                    daemon=True,
                    args=[connection_pool]
                )
                maintenance_thread.start()
            return True

        except Error as e:
            messagebox.showerror(
                title="Error",
                message=f"Error al conectar a pool MySQL: {e}"
            )
            return False


def get_connection():
    """
    Obtiene una conexión del pool. Si el pool no existe, intenta inicializarlo.
    """
    global connection_pool
    
    with pool_lock:
        if connection_pool is None:
            success = init_connection_pool()
            if not success:
                print("No se pudo obtener conexión - pool no inicializado")
                return None
    
    try:
        connection = connection_pool.get_connection()
        return connection
    except Exception as e:
        print(f"Error al obtener conexión del pool: {e}")
        return None
    
    
def _maintain_pool(connection_pool):
    """
    Función interna que mantiene vivo el pool de conexiones
    """
    while True:
        time.sleep(59)  # Verificar cada minuto
        with pool_lock:
            if connection_pool is None:
                # El pool ya no existe, terminar el hilo
                return
            
            try:
                # Obtener una conexión para probar el pool
                conn = connection_pool.get_connection()
                conn.ping(reconnect=True)
                conn.close()
                print("Pool de conexiones verificado - OK")
            except Exception as e:
                print(f"Error en el mantenimiento del pool: {e}")

def close_all_connections():
    """
    Cierra el pool de conexiones completo
    """
    global connection_pool
    
    with pool_lock:
        if connection_pool is not None:
            print("Cerrando el pool de conexiones")
            connection_pool = None