def get_pagos_con_detalles(connection, correspondencia="%"):
    if not isinstance(correspondencia,str):
        correspondencia="%"
    if correspondencia == "Todos":
        correspondencia = "%"
    try:
        cursor = connection.cursor()

        sql_query = f"""
            SELECT pago. id, alumno.nombre, alumno.apellido, materia.denominacion, pago.monto, pago.cuota, pago.fecha
            FROM pago
            JOIN alumno ON pago.id_alumno = alumno.id
            JOIN materia ON pago.id_materia = materia.id
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
        return