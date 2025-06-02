from db.conexion import crear_conexion

class SucursalModel:
    def __init__(self):
        self.conexion = crear_conexion()

    def obtener_todas(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM sucursal")
            return cursor.fetchall()

    def agregar(self, nombre, direccion, ciudad, estado, codigo_postal, telefono):
        with self.conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO sucursal (nombre, direccion, ciudad, estado, codigo_postal, telefono) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, direccion, ciudad, estado, codigo_postal, telefono)
            )
            self.conexion.commit()
            return cursor.lastrowid

    def actualizar(self, id_sucursal, nombre, direccion, ciudad, estado, codigo_postal, telefono):
        with self.conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE sucursal SET nombre=%s, direccion=%s, ciudad=%s, estado=%s, "
                "codigo_postal=%s, telefono=%s WHERE id_sucursal=%s",
                (nombre, direccion, ciudad, estado, codigo_postal, telefono, id_sucursal)
            )
            self.conexion.commit()
            return cursor.rowcount

    def eliminar(self, id_sucursal):
        with self.conexion.cursor() as cursor:
            cursor.execute("DELETE FROM sucursal WHERE id_sucursal=%s", (id_sucursal,))
            self.conexion.commit()
            return cursor.rowcount

    def __del__(self):
        if hasattr(self, 'conexion') and self.conexion:
            self.conexion.close()