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
        INSERT INTO inscripcion (id_alumno, id_materia, n_cuotas, monto_cuota, paga_el, monto_cuota_recargo, estado, mes, año)
        VALUES (%s, %s, 5, 1000, 10, 1100, 'curso', 1, 2025)
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
        WHERE id_inscripcion = (
            SELECT DISTINCT id
            FROM inscripcion
            WHERE id_alumno = %s
            AND id_materia = %s
            AND estado = 'curso'
        )
        AND cuota NOT IN (
            SELECT cuota 
            FROM deuda
            WHERE id_inscripcion = (
                SELECT DISTINCT id
                FROM inscripcion
                WHERE id_alumno = %s
                AND id_materia = %s
            )
            AND estado = 'pendiente'
        );
        """
        cursor.execute(sql_query, (alumno, materia, alumno, materia))
        
        cuotas = cursor.fetchall()
        if len(cuotas) == 0:
            return [0]
        else:
            return [cuota[0] for cuota in cuotas]
    except Exception as e:
        print(f"Error al obtener pagos: {e}")
        return []
    
def editar_alumno(connection, id, nombre, apellido, dni, calle, numero, email, telefono):
    try:
        cursor = connection.cursor()
        sql_query = """
            UPDATE alumno
            SET nombre = %s, apellido = %s,
            dni = %s, dir_calle = %s, dir_numero = %s,
            email = %s, telefono = %s
            WHERE id = %s
        """
        cursor.execute(sql_query, (nombre, apellido, dni, calle, numero, email, telefono, id))
        connection.commit()
        return "Alumno editado correctamente"
    except Exception as e:
        print(f"Error al editar alumno: {e}")
        return
    finally:
        cursor.close()