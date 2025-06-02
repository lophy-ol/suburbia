import pymysql
from db.conexion import crear_conexion

class ArticuloModel:
    def __init__(self):
        self.conexion = crear_conexion()

    def obtener_categorias(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id_categorias, tipo_categoria FROM categoria")
            return cursor.fetchall()

    def obtener_marcas(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id_marca, nombre_marca FROM marcas")
            return cursor.fetchall()

    def obtener_articulos(self):
        with self.conexion.cursor() as cursor:
            query = """
                SELECT a.codigo_articulo, a.nombre_articulo, a.activacion_articulo, a.precio, a.stock,
                       c.tipo_categoria, m.nombre_marca, a.gasto
                FROM articulo a
                JOIN categoria c ON a.id_categorias = c.id_categorias
                JOIN marcas m ON a.id_marca = m.id_marca
            """
            cursor.execute(query)
            return cursor.fetchall()

    def agregar_articulo(self, codigo, nombre, activado, precio, stock, gasto, categoria, marca):
        try:
            # Validación adicional en el modelo
            if not isinstance(precio, (int, float)) or precio <= 0:
                raise ValueError("El precio debe ser un número positivo")
            if not isinstance(stock, int) or stock < 0:
                raise ValueError("El stock debe ser un entero no negativo")
                
            with self.conexion.cursor() as cursor:
                query = """
                    INSERT INTO articulo (codigo_articulo, nombre_articulo, activacion_articulo, 
                                        precio, stock, gasto, id_categorias, id_marca)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (codigo, nombre, activado, precio, stock, gasto, categoria, marca))
                self.conexion.commit()
        except pymysql.Error as e:
            raise Exception(f"Error de base de datos: {e}")
        except Exception as e:
            raise Exception(f"Error al agregar artículo: {e}")

    def actualizar_articulo(self, codigo, nombre, activado, precio, stock, gasto, categoria, marca):
        with self.conexion.cursor() as cursor:
            query = """
                UPDATE articulo
                SET nombre_articulo=%s, activacion_articulo=%s, precio=%s, 
                    stock=%s, gasto=%s, id_categorias=%s, id_marca=%s
                WHERE codigo_articulo=%s
            """
            cursor.execute(query, (nombre, activado, precio, stock, gasto, categoria, marca, codigo))
            self.conexion.commit()

    def obtener_articulo_por_codigo(self, codigo_articulo):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT nombre_articulo, precio FROM articulo WHERE codigo_articulo = %s", (codigo_articulo,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener artículo: {e}")
            return None

    def eliminar_articulo(self, codigo):
        with self.conexion.cursor() as cursor:
            # Forzar a string para evitar errores de tipo
            codigo_str = str(codigo)
            query = "DELETE FROM articulo WHERE codigo_articulo = %s"
            cursor.execute(query, (codigo_str,))
            self.conexion.commit()

    def __del__(self):
        self.conexion.close()

# Ejemplo de uso
modelo = ArticuloModel()
categorias = modelo.obtener_categorias()
marcas = modelo.obtener_marcas()
print("Categorias:", categorias)
print("Marcas:", marcas)