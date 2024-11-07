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

def get_alumnos(connection):
    try:
        cursor = connection.cursor()
        sql_select_query = "SELECT * FROM alumno"
        cursor.execute(sql_select_query)
        alumnos = cursor.fetchall()
        return alumnos
    except Exception as e:
        print(f"Error al obtener alumnos: {e}")
        return []
    
def get_cuotas_por_alumno_materia(connection, alumno = "NULL", materia = "NULL"):
    try:
        cursor = connection.cursor()

        sql_query = """
            SELECT cuota FROM pago
            WHERE id_alumno = %s
            AND id_materia = %s
        """
        cursor.execute(sql_query, (alumno, materia))
        
        cuotas = cursor.fetchall()
        if len(cuotas) == 0:
            return [0]
        else:
            return [cuota[0] for cuota in cuotas]
    except Exception as e:
        print(f"Error al obtener pagos: {e}")
        return []
    