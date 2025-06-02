from db.conexion import crear_conexion

class CategoriasModel:
    def __init__(self):
        self.conexion = crear_conexion()

    def obtener_todas(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM categoria")
            return cursor.fetchall()

    def agregar(self, tipo_categoria):
        with self.conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO categoria (tipo_categoria) VALUES (%s)",
                (tipo_categoria,)
            )
            self.conexion.commit()
            return cursor.lastrowid

    def actualizar(self, id_categoria, tipo_categoria):
        with self.conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE categoria SET tipo_categoria=%s WHERE id_categorias=%s",
                (tipo_categoria, id_categoria)
            )
            self.conexion.commit()
            return cursor.rowcount

    def eliminar(self, id_categoria):
        with self.conexion.cursor() as cursor:
            cursor.execute(
                "DELETE FROM categoria WHERE id_categorias=%s",
                (id_categoria,)
            )
            self.conexion.commit()
            return cursor.rowcount

    def __del__(self):
        self.conexion.close()