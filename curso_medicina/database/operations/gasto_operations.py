def insert_gasto(connection, monto, divisa, correspondencia, descripcion, id_usuario):
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO gasto (monto, divisa, fecha, correspondencia, descripcion, id_usuario) 
        VALUES (%s, %s, CURDATE(), %s, %s, %s)
        """
        cursor.execute(sql_insert_query, (monto, divisa, correspondencia, descripcion, id_usuario))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error al insertar gasto: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()