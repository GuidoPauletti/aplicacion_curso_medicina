from tkinter import messagebox

def call_update_debts(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CALL update_student_debts()")
        connection.commit()
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al validar credenciales: {e}"
        )
        connection.rollback()
        return None
    finally:
        cursor.close()