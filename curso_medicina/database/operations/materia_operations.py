def get_materias(connection):
    try:
        cursor = connection.cursor()
        sql_select_query = "SELECT id, denominacion FROM materia"
        cursor.execute(sql_select_query)
        materias = [f'{row[0]} - {row[1]}' for row in cursor.fetchall()]
        return materias
    except Exception as e:
        print(f"Error al obtener materias: {e}")
        return []

def get_materias_por_alumno(connection, id_alumno):
    """Obtiene las materias en las que está inscrito un alumno dado su ID."""
    try:
        cursor = connection.cursor()
        sql_select_query = """
        SELECT m.id, m.denominacion 
        FROM materia m
        JOIN inscripcion i ON m.id = i.id_materia
        WHERE i.id_alumno = %s AND i.estado = 'curso'
        """
        cursor.execute(sql_select_query, (id_alumno,))
        materias = cursor.fetchall()
        return materias
    except Exception as e:
        print(f"Error al obtener materias para el alumno {id_alumno}: {e}")
        return []