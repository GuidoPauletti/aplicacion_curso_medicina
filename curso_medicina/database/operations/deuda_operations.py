def call_update_debts(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CALL update_student_debts()")
        connection.commit()
    except Exception as e:
        print(f"Error al calcular deudas: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()