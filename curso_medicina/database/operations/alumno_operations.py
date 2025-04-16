from curso_medicina.database.connection import get_connection

from tkinter import messagebox

def insert_alumno(nombre, apellido, dni, email, telefono, dir_calle, dir_numero):
    try:
        connection = get_connection()
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
        connection.close()

def insert_alumno_materia(alumno_id, materia_id, tipo_inscripcion_id):
    try:
        connection = get_connection()
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
        connection.close()

def get_alumnos(page = 1, per_page = 20):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Calcular offset
        offset = (page - 1) * per_page

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
            alumno a
        LIMIT %s OFFSET %s;
        """
        cursor.execute(sql_select_query, (per_page, offset))
        alumnos = cursor.fetchall()

        count_query = "SELECT COUNT(*) FROM alumno"
        cursor.execute(count_query)
        total = cursor.fetchall()[0][0]

        return alumnos, total
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener alumnos: {e}"
        )
        return []
    finally:
        cursor.close()
        connection.close()

def get_alumnos_filtrados(filtro):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        qry = f"""
        SELECT id, nombre, apellido
        FROM alumno
        WHERE
        LOWER(nombre) LIKE '{filtro}%'
        OR LOWER(apellido) LIKE '{filtro}%'
        LIMIT 10
        """

        cursor.execute(qry)
        alumnos = cursor.fetchall()

        return alumnos
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener alumnos filtrados: {e}"
        )
    finally:
        cursor.close()
        connection.close()


def get_unico_alumno(id_alumno):
    try:
        connection = get_connection()
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
            alumno a
        WHERE a.id = %s;
        """
        cursor.execute(sql_select_query, (id_alumno,))
        alumno = cursor.fetchone()
        return alumno
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener alumnos: {e}"
        )
        return []
    finally:
        cursor.close()
        connection.close()

def get_alumnos_por_materia(materia, page = 1, per_page = 20):
    if materia == "Todas":
        return get_alumnos(page, per_page)
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Calcular offset
        offset = (page - 1) * per_page

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
            END AS tiene_deuda_pendiente,
            m.denominacion
        FROM 
            alumno a
        LEFT JOIN inscripcion i ON a.id = i.id_alumno
        LEFT JOIN materia m ON i.id_materia = m.id
        WHERE m.denominacion LIKE %s
        LIMIT %s OFFSET %s;
        """
        cursor.execute(sql_select_query, (materia, per_page, offset))
        alumnos = cursor.fetchall()

        qry_total = """
        SELECT COUNT(*) FROM alumno a
        LEFT JOIN inscripcion i ON a.id = i.id_alumno
        LEFT JOIN materia m ON i.id_materia = m.id
        WHERE m.denominacion LIKE %s
        """
        cursor.execute(qry_total, (materia,))
        total = cursor.fetchall()[0][0]

        return alumnos, total
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener alumnos por materia: {e}"
        )
        return []
    finally:
        cursor.close()
        connection.close()
    
def get_cuotas_por_alumno_materia(alumno = "NULL", materia = "NULL"):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql_query = """
        SELECT i.id, ii.monto_cuota, SUM(p.monto) monto_pago, p.cuota, COALESCE(d.estado,'saneada') deuda
        FROM inscripcion i
        LEFT JOIN info_inscripcion ii ON ii.id = i.id_info_inscripcion
        JOIN pago p ON p.id_inscripcion = i.id
        LEFT JOIN deuda d ON d.id_inscripcion = p.id_inscripcion AND d.cuota = p.cuota
        WHERE i.id = (
                    SELECT DISTINCT id
                    FROM inscripcion
                    WHERE id_alumno = %s
                    AND id_materia = %s
                    AND estado = 'curso'
                )
        GROUP BY id, monto_cuota, cuota, deuda
        HAVING monto_pago >= monto_cuota AND deuda = 'saneada';
        """
        cursor.execute(sql_query, (alumno, materia))
        
        cuotas = cursor.fetchall()
        if len(cuotas) == 0:
            return [0]
        else:
            return [cuota[3] for cuota in cuotas]
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener cuotas de alumno: {e}"
        )
        return []
    finally:
        cursor.close()
        connection.close()
    
def editar_alumno(id, nombre, apellido, dni, calle, numero, email, telefono):
    try:
        connection = get_connection()
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
        connection.close()

def editar_dia_de_pago_alumno(id, paga_el):
    try:
        connection = get_connection()
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
        connection.close()

def get_inscripciones_alumno(id_alumno):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_select_query = """
        SELECT i.id, m.denominacion, ii.descripcion, i.paga_el,
            COALESCE(d.monto, 0) deuda,
            SUM(COALESCE(p.monto,0)) AS pagado,
            i.estado estado,
            CASE
				WHEN d.monto IS NULL THEN 'No'
                WHEN d.monto IS NOT NULL THEN 'Si'
			END tiene_deuda
        FROM alumno a
        LEFT JOIN inscripcion i ON a.id = i.id_alumno
        LEFT JOIN materia m ON m.id = i.id_materia
        LEFT JOIN info_inscripcion ii ON ii.id = i.id_info_inscripcion
        LEFT JOIN (SELECT * FROM deuda WHERE estado = 'pendiente') d ON d.id_inscripcion = i.id
        LEFT JOIN pago p ON d.id_inscripcion = p.id_inscripcion AND d.cuota = p.cuota
        WHERE a.id = %s
        GROUP BY id, denominacion, descripcion, paga_el, deuda, estado, tiene_deuda
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
    finally:
        cursor.close()
        connection.close()