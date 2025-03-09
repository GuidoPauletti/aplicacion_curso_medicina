from curso_medicina.database.connection import get_connection

from tkinter import messagebox

def get_info_inscripciones():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql_query = f"SELECT * FROM info_inscripcion"
        cursor.execute(sql_query)
        
        tipos_inscripcion = cursor.fetchall()
        return tipos_inscripcion
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener tipos de inscripcion: {e}"
        )
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def get_info_inscripcion(id_inscripcion):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql_query = """
        SELECT ii.monto_cuota, ii.monto_cuota_recargo, ii.n_cuotas, ii.descripcion
        FROM inscripcion i
        LEFT JOIN info_inscripcion ii
        ON i.id_info_inscripcion = ii.id
        WHERE i.id = %s
        """
        cursor.execute(sql_query, (id_inscripcion,))
        
        info_inscripcion = cursor.fetchone()
        return info_inscripcion
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener info de inscripcion: {e}"
        )
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def get_descripciones():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_insert_query = """
        SELECT id, descripcion
        FROM info_inscripcion
        """
        cursor.execute(sql_insert_query)
        descripciones = cursor.fetchall()
        return descripciones
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al traer descripcion de inscripciones: {e}"
        )
        return None
    finally:
        cursor.close()
        connection.close()

def get_detalle_tipo_inscripcion(id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_insert_query = """
        SELECT *
        FROM info_inscripcion
        WHERE id = %s
        """
        cursor.execute(sql_insert_query, (id,))
        detalle_tipo_inscripcion = cursor.fetchone()
        return detalle_tipo_inscripcion
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al traer detalle de tipo de inscripcion: {e}"
        )
        return None
    finally:
        cursor.close()
        connection.close()

def get_inscripcion_alumno_materia(id_alumno, id_materia):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_insert_query = """
        SELECT DISTINCT i.id, ii.n_cuotas
        FROM inscripcion i INNER JOIN info_inscripcion ii
        ON i.id_info_inscripcion = ii.id
        WHERE id_alumno = %s AND id_materia = %s AND i.estado = 'curso'
        """
        cursor.execute(sql_insert_query, (id_alumno, id_materia))
        inscripcion = cursor.fetchone()
        return inscripcion
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al traer detalle de tipo de inscripcion: {e}"
        )
        return None
    finally:
        cursor.close()
        connection.close()


def save_tipo_inscripcion(descripcion, cuota, cuota_recargo, n_cuotas):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO info_inscripcion(descripcion, monto_cuota, monto_cuota_recargo, n_cuotas)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_insert_query, (descripcion, cuota, cuota_recargo, n_cuotas))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al crear tipo de inscripción: {e}"
        )
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def editar_tipo_inscripcion(id, descripcion, cuota, cuota_recargo, n_cuotas):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_query = """
            UPDATE info_inscripcion
            SET descripcion = %s, monto_cuota = %s, monto_cuota_recargo = %s, n_cuotas = %s
            WHERE id = %s
        """
        cursor.execute(sql_query, (descripcion, cuota, cuota_recargo, n_cuotas, id))
        connection.commit()
        return "Tipo de inscripcion editado correctamente"
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al editar el tipo de inscripcion: {e}"
        )
        connection.rollback()
        return
    finally:
        cursor.close()
        connection.close()

def finalizar_inscripcion(id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_query = """
            UPDATE inscripcion
            SET estado = 'finalizado'
            WHERE id = %s
        """
        cursor.execute(sql_query, (id,))
        connection.commit()
        return "Inscripcion finalizada correctamente"
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al editar el tipo de inscripcion: {e}"
        )
        connection.rollback()
        return
    finally:
        cursor.close()
        connection.close()
    
def editar_inscripcion(id_inscripcion, tipo, paga_el, estado):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_query = """
            UPDATE inscripcion
            SET id_info_inscripcion = (SELECT MAX(id) FROM info_inscripcion WHERE descripcion = %s), paga_el = %s, estado = %s
            WHERE id = %s
        """
        cursor.execute(sql_query, (tipo, paga_el, estado, id_inscripcion))
        connection.commit()
        return "Inscripcion editada correctamente"
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al editar la inscripcion: {e}"
        )
        connection.rollback()
        return
    finally:
        cursor.close()
        connection.close()