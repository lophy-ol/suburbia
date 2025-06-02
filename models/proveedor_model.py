from db.conexion import crear_conexion

class ProveedorModel:
    def __init__(self):
        self.conexion = crear_conexion()

    def obtener_proveedores(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM proveedor")
            return cursor.fetchall()

    def agregar_proveedor(self, rfc, nombre, telefono, correo, direccion):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO proveedor (RFC, nombre, telefono, correo, direccion) VALUES (%s, %s, %s, %s, %s)",
                    (rfc, nombre, telefono, correo, direccion)
                )
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al agregar proveedor: {e}")
            return False

    def actualizar_proveedor(self, rfc, nombre, telefono, correo, direccion):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(
                    "UPDATE proveedor SET nombre=%s, telefono=%s, correo=%s, direccion=%s WHERE RFC=%s",
                    (nombre, telefono, correo, direccion, rfc)
                )
                filas_afectadas = cursor.rowcount
            self.conexion.commit()
            if filas_afectadas == 0:
                print("No se encontró el RFC para actualizar.")
                return False
            return True
        except Exception as e:
            print(f"Error al actualizar proveedor: {e}")
            return False

    def eliminar_proveedor(self, rfc):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("DELETE FROM proveedor WHERE RFC=%s", (rfc,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar proveedor: {e}")
            return False

    def __del__(self):
        if hasattr(self, 'conexion') and self.conexion:
            self.conexion.close()