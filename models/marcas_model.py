from db.conexion import crear_conexion
import pymysql

class MarcasModel:
    def __init__(self):
        self.conexion = crear_conexion()
        self.cursor = self.conexion.cursor()

    def obtener_todas_marcas(self):
        try:
            self.cursor.execute("""
                SELECT marcas.id_marca, marcas.nombre_marca, proveedor.nombre
                FROM marcas
                JOIN proveedor ON marcas.RFC = proveedor.RFC
            """)
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener marcas: {e}")

    def obtener_proveedores(self):
        try:
            with self.conexion.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT RFC, nombre FROM proveedor")
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener proveedores: {e}")

    def agregar_marca(self, nombre_marca, rfc):
        try:
            print(f"RFC que se va a guardar en marcas: '{rfc}'")
            with self.conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO marcas (nombre_marca, RFC) VALUES (%s, %s)",
                    (nombre_marca, rfc)
                )
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al agregar marca: {e}")

    def actualizar_marca(self, id_marca, nombre_marca, rfc):
        try:
            self.cursor.execute(
                "UPDATE marcas SET nombre_marca=%s, RFC=%s WHERE id_marca=%s",
                (nombre_marca, rfc, id_marca)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al actualizar marca: {e}")

    def eliminar_marca(self, id_marca):
        try:
            self.cursor.execute(
                "DELETE FROM marcas WHERE id_marca=%s",
                (id_marca,)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al eliminar marca: {e}")

    def __del__(self):
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'conexion') and self.conexion:
                self.conexion.close()
        except Exception:
            pass
