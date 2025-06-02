from db.conexion import crear_conexion

class EmpleadoModel:
    @staticmethod
    def obtener_todos():
        conexion = crear_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT e.id_empleado, e.nombre_empleado, e.apellido_empleado , e.telefono, e.correo, 
                           e.direccion, s.id_sucursal AS sucursal
                    FROM empleado e
                    JOIN sucursal s ON e.id_sucursal = s.id_sucursal
                """)
                return cursor.fetchall()
        finally:
            conexion.close()

    @staticmethod
    def agregar(nombre, apellido, cargo, fecha, salario, id_sucursal):
        conexion = crear_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO empleado (Nombre, Apellido, Cargo, Fecha_Contratacion, Salario, id_sucursal)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nombre, apellido, cargo, fecha, salario, id_sucursal))
                conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def actualizar(id_empleado, nombre, apellido, cargo, fecha, salario, id_sucursal):
        conexion = crear_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    UPDATE empleado
                    SET Nombre=%s, Apellido=%s, Cargo=%s, Fecha_Contratacion=%s, Salario=%s, id_sucursal=%s
                    WHERE id_empleado=%s
                """, (nombre, apellido, cargo, fecha, salario, id_sucursal, id_empleado))
                conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        conexion = crear_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM empleado WHERE id_empleado=%s", (id_empleado,))
                conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def obtener_sucursales():
        conexion = crear_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_sucursal, nombre FROM sucursal")
                return cursor.fetchall()
        finally:
            conexion.close()