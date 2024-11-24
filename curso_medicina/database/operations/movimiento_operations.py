def get_movimientos_con_detalles(connection, ventana_temporal):
    """Obtiene informacion de movimientos dentro de la ventana temporal"""
    condicion = {
        "Ultimo día" : "= CURDATE()",
        "Ultima semana" : ">= DATE_SUB(CURDATE(), INTERVAL 7 DAY)",
        "Ultimo mes": ">= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)"
    }
    try:
        cursor = connection.cursor()
        sql_query = f"""
        SELECT 
            g.id AS ID,
            'Salida' AS Tipo,
            g.monto AS Monto,
            g.divisa AS Divisa,
            g.descripcion AS Descripción,
            g.correspondencia AS Cuenta,
            g.fecha AS Fecha
        FROM 
            gasto g
        WHERE Fecha {condicion[ventana_temporal]}

        UNION

        SELECT 
            p.id AS ID,
            'Entrada' AS Tipo,
            p.monto AS Monto,
            p.divisa AS Divisa,
            CONCAT(a.nombre, ' ', a.apellido, ' - Cuota ', p.cuota, ' de ', m.denominacion) AS Descripción,
            p.correspondencia AS Cuenta,
            p.fecha AS Fecha
        FROM 
            pago p
        JOIN
            inscripcion i ON p.id_inscripcion = i.id
        JOIN 
            alumno a ON i.id_alumno = a.id
        JOIN 
            materia m ON i.id_materia = m.id
        WHERE Fecha {condicion[ventana_temporal]}

        ORDER BY 
            Fecha DESC;
        """
        cursor.execute(sql_query)
        movimientos = cursor.fetchall()
        return movimientos
    except Exception as e:
        print(f"Error al obtener movimientos: {e}")
        connection.rollback()
        return []
    finally:
        cursor.close()