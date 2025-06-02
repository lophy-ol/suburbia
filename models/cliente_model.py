from db.conexion import crear_conexion

class ClienteModel:
    @staticmethod
    def obtener_todos():
        conexion = crear_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM cliente")
                return cursor.fetchall()
        finally:
            conexion.close()

    @staticmethod
    def agregar_cliente(nombre, apellido, telefono, correo, direccion):
        conexion = crear_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO cliente (Nombre, Apellido, Telefono, Correo, Direccion)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre, apellido, telefono, correo, direccion))
                conexion.commit()
                return True
        except Exception as e:
            print(f"Error al agregar cliente: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def actualizar_cliente(id_cliente, nombre, apellido, telefono, correo, direccion):
        conexion = crear_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    UPDATE cliente SET 
                    Nombre=%s, Apellido=%s, Telefono=%s, Correo=%s, Direccion=%s
                    WHERE id_cliente=%s
                """, (nombre, apellido, telefono, correo, direccion, id_cliente))
                conexion.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def eliminar_cliente(id_cliente):
        conexion = crear_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM cliente WHERE id_cliente=%s", (id_cliente,))
                conexion.commit()
                return True
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False
        finally:
            conexion.close()