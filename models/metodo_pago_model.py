import pymysql
from db.conexion import crear_conexion

class MetodoPagoModel:
    def __init__(self):
        self.conexion = crear_conexion()

    def obtener_metodos_pago(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id_modo_pago, tipo FROM metodo_pago")
            return cursor.fetchall()

    def agregar_metodo_pago(self, tipo):
        try:
            if not tipo or not isinstance(tipo, str):
                raise ValueError("El tipo de método de pago debe ser una cadena no vacía")
            
            with self.conexion.cursor() as cursor:
                query = "INSERT INTO metodo_pago (tipo) VALUES (%s)"
                cursor.execute(query, (tipo,))
                self.conexion.commit()
        except pymysql.Error as e:
            raise Exception(f"Error de base de datos: {e}")
        except Exception as e:
            raise Exception(f"Error al agregar método de pago: {e}")

    def actualizar_metodo_pago(self, id_modo_pago, tipo):
        try:
            if not tipo or not isinstance(tipo, str):
                raise ValueError("El tipo de método de pago debe ser una cadena no vacía")

            with self.conexion.cursor() as cursor:
                query = "UPDATE metodo_pago SET tipo = %s WHERE id_modo_pago = %s"
                cursor.execute(query, (tipo, id_modo_pago))
                self.conexion.commit()
        except pymysql.Error as e:
            raise Exception(f"Error de base de datos: {e}")
        except Exception as e:
            raise Exception(f"Error al actualizar método de pago: {e}")

    def eliminar_metodo_pago(self, id_modo_pago):
        try:
            with self.conexion.cursor() as cursor:
                query = "DELETE FROM metodo_pago WHERE id_modo_pago = %s"
                cursor.execute(query, (id_modo_pago,))
                self.conexion.commit()
        except pymysql.Error as e:
            raise Exception(f"Error de base de datos: {e}")
        except Exception as e:
            raise Exception(f"Error al eliminar método de pago: {e}")

    def __del__(self):
        self.conexion.close()

# Ejemplo de uso
if __name__ == "__main__":
    modelo = MetodoPagoModel()
    metodos = modelo.obtener_metodos_pago()
    print("Métodos de pago:", metodos)
