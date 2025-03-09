from curso_medicina.database.connection import get_connection

from tkinter import messagebox

def insert_gasto(monto, divisa, correspondencia, descripcion, id_usuario, metodo):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO gasto (monto, divisa, fecha, correspondencia, descripcion, id_usuario, metodo) 
        VALUES (%s, %s, CURDATE(), %s, %s, %s, %s)
        """
        cursor.execute(sql_insert_query, (monto, divisa, correspondencia, descripcion, id_usuario, metodo))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al insertar gasto: {e}"
        )
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def get_gastos_con_detalles(correspondencia="%"):
    if not isinstance(correspondencia,str):
        correspondencia="%"
    if correspondencia == "Todos":
        correspondencia = "%"
    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql_query = f"""
            SELECT g.id, g.monto, g.divisa, g.fecha, g.correspondencia, g.metodo, g.descripcion, u.nombre responsable
            FROM gasto g INNER JOIN usuario u
            ON g.id_usuario = u.id
            WHERE g.correspondencia LIKE '{correspondencia}'
            ORDER BY fecha DESC
        """
        cursor.execute(sql_query)
        
        gastos = cursor.fetchall()
        return gastos
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener gastos: {e}"
        )
        return []
    finally:
        cursor.close()
        connection.close()

def borrar_gasto(id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql_query = """
            DELETE FROM gasto
            WHERE id = %s
        """
        cursor.execute(sql_query, (id,))
        connection.commit()
        return "Registro de gasto eliminado correctamente"
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al borrar el gasto: {e}"
        )
        return
    finally:
        cursor.close()
        connection.close()

def editar_gasto(id, monto, correspondencia, metodo, descripcion, usuario):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_query = """
            UPDATE gasto
            SET monto = %s, correspondencia = %s, metodo = %s, descripcion = %s, id_usuario = %s
            WHERE id = %s
        """
        cursor.execute(sql_query, (monto, correspondencia, metodo, descripcion, usuario, id))
        connection.commit()
        return "Registro de gasto editado correctamente"
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al editar el gasto: {e}"
        )
        return
    finally:
        cursor.close()
        connection.close()