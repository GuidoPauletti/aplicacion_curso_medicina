from curso_medicina.database.connection import init_connection_pool, close_all_connections
from curso_medicina.gui.app import Aplicacion

import time
import tkinter as tk
import atexit

import mysql.connector


def mantener_conexion_activa(conexion):
    while True:
        time.sleep(120)  # Espera 2 minutos
        try:
            conexion.ping(reconnect=True)
        except mysql.connector.Error as err:
            return


def main():
    init_connection_pool()

    # Registrar la función para cerrar el pool al salir
    atexit.register(close_all_connections)

    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    