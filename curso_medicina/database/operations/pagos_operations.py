from tkinter import messagebox

def get_pagos_con_detalles(connection, correspondencia="%", alumno = None):
    if not isinstance(correspondencia,str):
        correspondencia="%"
    if correspondencia == "Todos":
        correspondencia = "%"
    try:
        cursor = connection.cursor()

        if alumno:
            sql_query = f"""
                SELECT p.id, a.nombre, a.apellido, m.denominacion, p.monto, p.metodo, p.correspondencia ,p.cuota, p.fecha, u.nombre, p.observaciones
                FROM pago p
                JOIN inscripcion ON p.id_inscripcion = inscripcion.id
                JOIN alumno a ON inscripcion.id_alumno = a.id
                JOIN materia m ON inscripcion.id_materia = m.id
                JOIN usuario u ON p.id_usuario = u.id
                WHERE p.correspondencia LIKE '{correspondencia}'
                AND inscripcion.id_alumno = {alumno}
                ORDER BY fecha DESC
            """
        else:
            sql_query = f"""
                SELECT p.id, a.nombre, a.apellido, m.denominacion, p.monto, p.metodo, p.correspondencia , p.cuota, p.fecha, u.nombre, p.observaciones
                FROM pago p
                JOIN inscripcion ON p.id_inscripcion = inscripcion.id
                JOIN alumno a ON inscripcion.id_alumno = a.id
                JOIN materia m ON inscripcion.id_materia = m.id
                JOIN usuario u ON p.id_usuario = u.id 
                WHERE p.correspondencia LIKE '{correspondencia}'
                ORDER BY fecha DESC
            """
        cursor.execute(sql_query)
        
        pagos = cursor.fetchall()
        return pagos
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener pagos: {e}"
        )
        connection.rollback()
        return []
    finally:
        cursor.close()

def get_info_ultimo_pago(connection, id, cuota):
    try:
        cursor = connection.cursor()

        sql_query = """
            SELECT * FROM view_chequear_ultima_cuota
            WHERE id_inscripcion = (SELECT DISTINCT id_inscripcion FROM pago WHERE id = %s)
            AND cuota = %s
        """
        cursor.execute(sql_query, (id, cuota))
        info_pago = cursor.fetchall()
        return info_pago
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener info del pago: {e}"
        )
        return
    finally:
        cursor.close()
    
def borrar_pago(connection, id):
    try:
        cursor = connection.cursor()

        sql_query = f"""
            DELETE FROM pago
            WHERE id = {id}
        """
        cursor.execute(sql_query)
        connection.commit()
        return "Registro de pago eliminado correctamente"
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al borrar el pago: {e}"
        )
        return
    finally:
        cursor.close()
        

def editar_pago(connection, id, monto, cuota, metodo, correspondencia, id_usuario):
    try:
        cursor = connection.cursor()
        sql_query = f"""
            UPDATE pago
            SET monto = {monto}, cuota = {cuota}, id_usuario = {id_usuario}, metodo = '{metodo}', correspondencia = '{correspondencia}'
            WHERE id = {id}
        """
        cursor.execute(sql_query)
        connection.commit()
        return "Registro de pago editado correctamente"
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al editar el pago: {e}"
        )
        connection.rollback()
        return
    finally:
        cursor.close()
    
def insert_pago(connection, id_alumno, id_materia, monto, divisa, metodo, cuota, correspondencia, fecha, obs,id_usuario):
    try:
        cursor = connection.cursor()
        sql_insert_query = f"""
        INSERT INTO pago (id_inscripcion, monto, divisa, metodo, cuota, correspondencia, fecha, observaciones, id_usuario, cuota_de_mes) 
        VALUES (
            (SELECT DISTINCT id FROM inscripcion WHERE id_alumno = {id_alumno} AND id_materia = {id_materia} AND estado = 'curso'),
            {monto},
            '{divisa}',
            '{metodo}',
            {cuota},
            '{correspondencia}',
            '{fecha}',
            '{obs}',
            {id_usuario},
            {cuota} - 1 + (SELECT DISTINCT mes FROM inscripcion WHERE id_alumno = {id_alumno} AND id_materia = {id_materia} AND estado = 'curso')
        )
        """
        cursor.execute(sql_insert_query)
        connection.commit()
        pago_id = cursor.lastrowid  # Obtener el ID del pago insertado
        return pago_id
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al insertar pago: {e}"
        )
        return None
    finally:
        cursor.close()

def insert_pago_moneda_extranjera(connection, id_pago, divisa, monto):
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO pago_divisa_extranjera (pago_id, divisa, monto) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql_insert_query, (id_pago, divisa, monto))
        connection.commit()
        return
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al insertar pago en divisa extranjera: {e}"
        )
        return None
    finally:
        cursor.close()