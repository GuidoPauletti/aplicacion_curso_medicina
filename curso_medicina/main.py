from curso_medicina.database.connection import create_connection
from curso_medicina.gui.app import Aplicacion

import threading
import time
import tkinter as tk
import mysql.connector

def mantener_conexion_activa(conexion):
    while True:
        time.sleep(120)  # Espera 2 minutos
        try:
            conexion.ping(reconnect=True)
        except mysql.connector.Error as err:
            return
            # Aquí puedes intentar reconectar o manejar el error según sea necesario

def main():
    conn = create_connection()
    hilo_mantenimiento = threading.Thread(target=mantener_conexion_activa, args=(conn,), daemon=True)
    hilo_mantenimiento.start()
    root = tk.Tk()
    app = Aplicacion(root, conn)
    root.mainloop()

if __name__ == "__main__":
    main()
    