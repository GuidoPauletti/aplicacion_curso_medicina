from curso_medicina.database.connection import get_connection

from tkinter import messagebox

def get_movimientos_con_detalles(desde, hasta):
    """Obtiene informacion de movimientos dentro de la ventana temporal"""

    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql_query = f"""
        SELECT 
            g.id AS ID,
            'Salida' AS Tipo,
            g.monto AS Monto,
            CONCAT(g.divisa, ' (', g.metodo, ')') AS Divisa,
            g.descripcion AS Descripción,
            g.correspondencia AS Cuenta,
            g.fecha AS Fecha
        FROM 
            gasto g
        WHERE DATE(g.fecha) >= '{desde}' AND DATE(g.fecha) <= '{hasta}'

        UNION

        SELECT 
            p.id AS ID,
            'Entrada' AS Tipo,
            CASE
                WHEN p.divisa != 'Peso' THEN pde.monto
                ELSE p.monto
            END AS Monto,
            CONCAT(p.divisa, ' (', p.metodo, ')') AS Divisa,
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
        LEFT JOIN
            pago_divisa_extranjera pde ON p.id = pde.pago_id
        WHERE DATE(p.fecha) >= '{desde}' AND DATE(p.fecha) <= '{hasta}'

        ORDER BY 
            Fecha DESC;
        """
        cursor.execute(sql_query)
        movimientos = cursor.fetchall()
        return movimientos
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"Error al obtener movimientos: {e}"
        )
        connection.rollback()
        return []
    finally:
        cursor.close()
        connection.close()