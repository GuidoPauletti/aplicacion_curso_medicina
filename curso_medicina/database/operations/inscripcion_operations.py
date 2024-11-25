def get_descripciones(connection):
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        SELECT id, descripcion
        FROM info_inscripcion
        WHERE id != 2
        """
        cursor.execute(sql_insert_query)
        descripciones = cursor.fetchall()
        return descripciones
    except Exception as e:
        print(f"Error al traer descripcion de inscripciones: {e}")
        return None
    finally:
        cursor.close()