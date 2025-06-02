from db.conexion import crear_conexion

class VentasModel:
    def __init__(self):
        self.conexion = crear_conexion()

    def obtener_ventas(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM venta")
            return cursor.fetchall()

    def agregar_venta(self, id_venta, total, id_cliente, id_empleado, tipo_cliente,
                  codigo_articulo, cantidad, id_modo_pago, nombre_articulo):
        try:
            with self.conexion.cursor() as cursor:
                # Insertar la venta
                cursor.execute("""
                    INSERT INTO venta (
                        id_venta, total, id_cliente, id_empleado, tipo_cliente,
                        codigo_articulo, cantidad, id_modo_pago, nombre_articulo
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    id_venta, total, id_cliente, id_empleado, tipo_cliente,
                    codigo_articulo, cantidad, id_modo_pago, nombre_articulo
                ))

                # Actualizar el stock del artículo
                cursor.execute("""
                    UPDATE articulo
                    SET stock = stock - %s
                    WHERE codigo_articulo = %s
                """, (cantidad, codigo_articulo))

                cursor.execute("SELECT precio FROM articulo WHERE codigo_articulo = %s", (codigo_articulo,))
                resultado = cursor.fetchone()
                if not resultado:
                    print("Artículo no encontrado.")
                    return False
                precio_unitario = resultado["precio"]

            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al agregar venta: {e}")
            return False


    def actualizar_venta(self, id_venta, total, id_cliente, id_empleado, tipo_cliente,
                         codigo_articulo, cantidad, id_modo_pago, nombre_articulo):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("""
                    UPDATE venta
                    SET total=%s, id_cliente=%s, id_empleado=%s, tipo_cliente=%s,
                        codigo_articulo=%s, cantidad=%s, id_modo_pago=%s, nombre_articulo=%s
                    WHERE id_venta=%s
                """, (
                    total, id_cliente, id_empleado, tipo_cliente,
                    codigo_articulo, cantidad, id_modo_pago, nombre_articulo, id_venta
                ))
                filas_afectadas = cursor.rowcount
            self.conexion.commit()
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error al actualizar venta: {e}")
            return False

    def eliminar_venta(self, id_venta):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("DELETE FROM venta WHERE id_venta = %s", (id_venta,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar venta: {e}")
            return False

    def obtener_venta_por_id(self, id_venta):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM venta WHERE id_venta = %s", (id_venta,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener venta: {e}")
            return None

    # Métodos para obtener datos necesarios para los toggles en la vista

    def obtener_clientes(self):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT id_cliente, CONCAT(nombre, ' ', apellido) AS nombre_completo FROM clientes")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return []

    def obtener_empleados(self):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT id_empleado, CONCAT(nombre, ' ', apellido) AS nombre_completo FROM empleados")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return []

    def obtener_metodos_pago(self):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT id_modo_pago, tipo FROM metodo_pago")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener métodos de pago: {e}")
            return []

    def obtener_articulo_por_codigo(self, codigo_articulo):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT nombre, precio FROM articulos WHERE codigo_articulo = %s", (codigo_articulo,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener artículo: {e}")
            return None

    def __del__(self):
        if hasattr(self, 'conexion') and self.conexion:
            self.conexion.close()
