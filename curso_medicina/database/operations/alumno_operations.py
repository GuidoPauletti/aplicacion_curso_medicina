def insert_alumno(connection, nombre, apellido, dni, email, telefono, dir_calle, dir_numero):
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO alumno (nombre, apellido, dni, email, telefono, dir_calle, dir_numero) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert_query, (nombre, apellido, dni, email, telefono, dir_calle, dir_numero))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error al insertar alumno: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()

def insert_alumno_materia(connection, alumno_id, materia_id):
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO alumno_materia (id_alumno, id_materia)
        VALUES (%s, %s)
        """
        cursor.execute(sql_insert_query, (alumno_id, materia_id))
        connection.commit()
        return None
    except Exception as e:
        print(f"Error al inscribir alumno a materia/s: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()