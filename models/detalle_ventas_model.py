from db.conexion import crear_conexion

class DetalleVentaModel:
    def __init__(self):
        self.conexion = crear_conexion()

    def obtener_ventas(self):
        """Devuelve todas las ventas disponibles para mostrar en la lista."""
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT id_venta, total FROM ventas")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener ventas: {e}")
            return []

    def obtener_detalles_por_venta(self, id_venta):
        """Devuelve los detalles (artículos) de una venta específica."""
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        dv.id_detalles_ventas,
                        dv.id_venta,
                        dv.codigo_articulo,
                        a.nombre_articulo AS nombre_articulo,
                        dv.cantidad,
                        dv.importe,
                        (dv.cantidad * dv.importe) AS subtotal
                    FROM detalles_ventas dv
                    JOIN articulo a ON dv.codigo_articulo = a.codigo_articulo
                    WHERE dv.id_venta = %s
                """, (id_venta,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener detalles de venta: {e}")
            return []

    def eliminar_detalle(self, id_detalles_ventas):
        """Elimina un detalle de venta específico (si se desea editar/eliminar)."""
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("DELETE FROM detalles_ventas WHERE id_detalles_ventas = %s", (id_detalles_ventas,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar detalle de venta: {e}")
            return False

    def __del__(self):
        if hasattr(self, 'conexion') and self.conexion:
            self.conexion.close()
