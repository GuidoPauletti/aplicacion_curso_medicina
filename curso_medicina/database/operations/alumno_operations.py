from tkinter import messagebox

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
        messagebox.showerror(
            title="Error",
            message=f"Error al insertar alumno: {e}"
        )
        connection.rollback()
        return None
    finally:
        cursor.close()

def insert_alumno_materia(connection, alumno_id, materia_id, tipo_inscripcion_id):
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO inscripcion (id_alumno, id_materia, id_info_inscripcion, paga_el, estado, mes, año)
        VALUES (%s, %s, %s, 10, 'curso', (SELECT MONTH(CURDATE())), (SELECT YEAR(CURDATE())))
        """
        cursor.execute(sql_insert_query, (alumno_id, materia_id, tipo_inscripcion_id))
        connection.commit()
        return None
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al inscribir alumno a materia/s: {e}"
        )
        connection.rollback()
        return None
    finally:
        cursor.close()

def get_alumnos(connection):
    try:
        cursor = connection.cursor()
        sql_select_query = """
        SELECT 
            a.*,
            CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM inscripcion i
                    JOIN deuda d ON i.id = d.id_inscripcion
                    WHERE i.id_alumno = a.id AND d.estado = 'pendiente'
                ) THEN 'Si'
                ELSE 'No'
            END AS tiene_deuda_pendiente
        FROM 
            alumno a;
        """
        cursor.execute(sql_select_query)
        alumnos = cursor.fetchall()
        return alumnos
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener alumnos: {e}"
        )
        return []
    finally: cursor.close()
    
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
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener cuotas de alumno: {e}"
        )
        return []
    finally: cursor.close()
    
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
        messagebox.showerror(
            title="Error",
            message=f"Error al editar alumno: {e}"
        )
        return
    finally:
        cursor.close()

def editar_dia_de_pago_alumno(connection, id, paga_el):
    try:
        cursor = connection.cursor()
        sql_query = """
            UPDATE inscripcion
            SET paga_el = %s
            WHERE id_alumno = %s
        """
        cursor.execute(sql_query, (paga_el, id))
        connection.commit()
        return "Dia de pago editado correctamente"
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al editar dia de pago del alumno: {e}"
        )
        return
    finally:
        cursor.close()

def get_inscripciones_alumno(connection, id_alumno):
    try:
        cursor = connection.cursor()
        sql_select_query = """
        SELECT i.id, m.denominacion, ii.descripcion, i.paga_el, COALESCE(d.monto, 0) deuda, SUM(COALESCE(p.monto,0)) AS pagado
        FROM alumno a
        LEFT JOIN inscripcion i ON a.id = i.id_alumno
        LEFT JOIN materia m ON m.id = i.id_materia
        LEFT JOIN info_inscripcion ii ON ii.id = i.id_info_inscripcion
        LEFT JOIN (SELECT * FROM deuda WHERE estado = 'pendiente') d ON d.id_inscripcion = i.id
        LEFT JOIN pago p ON d.id_inscripcion = p.id_inscripcion AND d.cuota = p.cuota
        WHERE a.id = %s
        GROUP BY id, denominacion, descripcion, paga_el, deuda
        """
        cursor.execute(sql_select_query, (id_alumno,))
        alumnos = cursor.fetchall()
        return alumnos
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener inscripciones de alumno: {e}"
        )
        return []
    finally: cursor.close()