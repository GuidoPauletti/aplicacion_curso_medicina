def insert_alumno(connection, nombre, apellido, telefono):
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO alumno (nombre, apellido, telefono) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql_insert_query, (nombre, apellido, telefono))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error al insertar alumno: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()