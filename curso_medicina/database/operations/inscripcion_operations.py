def get_info_inscripciones(connection):
    try:
        cursor = connection.cursor()

        sql_query = f"SELECT * FROM info_inscripcion"
        cursor.execute(sql_query)
        
        tipos_inscripcion = cursor.fetchall()
        return tipos_inscripcion
    except Exception as e:
        print(f"Error al obtener tipos de inscripcion: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()

def get_descripciones(connection):
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        SELECT id, descripcion
        FROM info_inscripcion
        WHERE id != 2
        """
        cursor.execute(sql_insert_query)
        descripciones = cursor.fetchall()
        return descripciones
    except Exception as e:
        print(f"Error al traer descripcion de inscripciones: {e}")
        return None
    finally:
        cursor.close()

def get_detalle_tipo_inscripcion(connection, id):
    try:
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
        print(f"Error al traer detalle de tipo de inscripcion: {e}")
        return None
    finally:
        cursor.close()

def save_tipo_inscripcion(connection, descripcion, cuota, cuota_recargo, n_cuotas):
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO info_inscripcion(descripcion, monto_cuota, monto_cuota_recargo, n_cuotas)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_insert_query, (descripcion, cuota, cuota_recargo, n_cuotas))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error al crear tipo de inscripción: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()

def editar_tipo_inscripcion(connection, id, descripcion, cuota, cuota_recargo, n_cuotas):
    try:
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
        print(f"Error al editar el tipo de inscripcion: {e}")
        connection.rollback()
        return
    finally:
        cursor.close()