from curso_medicina.database.connection import get_connection

from tkinter import messagebox

def call_update_debts():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("CALL update_student_debts2()")
        connection.commit()
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al calcular las deudas: {e}"
        )
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def sanear_deuda(id_inscripcion, cuota):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_query = f"""
            UPDATE deuda
            SET estado = 'saneada'
            WHERE id_inscripcion = {id_inscripcion}
            AND cuota = {cuota}
        """
        cursor.execute(sql_query)
        connection.commit()
        messagebox.showinfo(
            title="Deuda saneada",
            message=f"Queda saneado el pago de la cuota {cuota}"
        )
        return "Exito"
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al sanear la cuenta: {e}"
        )
        connection.rollback()
        return
    finally:
        cursor.close()
        connection.close()