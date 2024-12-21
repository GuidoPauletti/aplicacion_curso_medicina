def get_pagos_con_detalles(connection, correspondencia="%", alumno = None):
    if not isinstance(correspondencia,str):
        correspondencia="%"
    if correspondencia == "Todos":
        correspondencia = "%"
    try:
        cursor = connection.cursor()

        if alumno:
            sql_query = f"""
                SELECT pago.id, alumno.nombre, alumno.apellido, materia.denominacion, pago.monto, pago.cuota, pago.fecha
                FROM pago
                JOIN inscripcion ON pago.id_inscripcion = inscripcion.id
                JOIN alumno ON inscripcion.id_alumno = alumno.id
                JOIN materia ON inscripcion.id_materia = materia.id
                WHERE pago.correspondencia LIKE '{correspondencia}'
                AND inscripcion.id_alumno = {alumno}
                ORDER BY fecha DESC
            """
        else:
            sql_query = f"""
                SELECT pago.id, alumno.nombre, alumno.apellido, materia.denominacion, pago.monto, pago.cuota, pago.fecha
                FROM pago
                JOIN inscripcion ON pago.id_inscripcion = inscripcion.id
                JOIN alumno ON inscripcion.id_alumno = alumno.id
                JOIN materia ON inscripcion.id_materia = materia.id
                WHERE pago.correspondencia LIKE '{correspondencia}'
                ORDER BY fecha DESC
            """
        cursor.execute(sql_query)
        
        pagos = cursor.fetchall()
        return pagos
    except Exception as e:
        print(f"Error al obtener pagos: {e}")
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
        print(f"Error al obtener info del pago: {e}")
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
        print(f"Error al borrar el pago: {e}")
        return
    finally:
        cursor.close()
        

def editar_pago(connection, id, monto, cuota):
    try:
        cursor = connection.cursor()
        sql_query = f"""
            UPDATE pago
            SET monto = {monto}, cuota = {cuota}
            WHERE id = {id}
        """
        cursor.execute(sql_query)
        connection.commit()
        return "Registro de pago editado correctamente"
    except Exception as e:
        print(f"Error al editar el pago: {e}")
        connection.rollback()
        return
    finally:
        cursor.close()
    
def insert_pago(connection, id_alumno, id_materia, monto, divisa, metodo, cuota, correspondencia, id_usuario):
    try:
        cursor = connection.cursor()
        sql_insert_query = f"""
        INSERT INTO pago (id_inscripcion, monto, divisa, metodo, cuota, correspondencia, fecha, id_usuario, cuota_de_mes) 
        VALUES (
            (SELECT DISTINCT id FROM inscripcion WHERE id_alumno = {id_alumno} AND id_materia = {id_materia} AND estado = 'curso'),
            {monto},
            '{divisa}',
            '{metodo}',
            {cuota},
            '{correspondencia}',
            CURDATE(),
            {id_usuario},
            {cuota} - 1 + (SELECT DISTINCT mes FROM inscripcion WHERE id_alumno = {id_alumno} AND id_materia = {id_materia} AND estado = 'curso')
        )
        """
        cursor.execute(sql_insert_query)
        connection.commit()
        pago_id = cursor.lastrowid  # Obtener el ID del pago insertado
        return pago_id
    except Exception as e:
        print(f"Error al insertar pago: {e}")
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
        print(f"Error al insertar pago en divisa extranjera: {e}")
        return None
    finally:
        cursor.close()