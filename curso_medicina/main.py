from curso_medicina.database.connection import create_connection
from curso_medicina.gui.app import Aplicacion
import tkinter as tk

def main():
    conn = create_connection()
    root = tk.Tk()
    app = Aplicacion(root, conn)
    root.mainloop()

if __name__ == "__main__":
    main()
    