from models.detalle_ventas_model import DetalleVentaModel
from models.articulo_model import ArticuloModel
from models.ventas_model import VentasModel

class DetalleVentaController:
    def __init__(self):
        self.model = DetalleVentaModel()
        self.articulo_model = ArticuloModel()
        self.venta_model = VentasModel()

    def obtener_ventas(self):
        """Devuelve una lista de ventas realizadas (id_venta y total)."""
        return self.venta_model.obtener_ventas()

    def obtener_detalles_por_venta(self, id_venta):
        """
        Devuelve detalles enriquecidos de una venta:
        incluye nombre del artículo, precio, cantidad, subtotal por detalle.
        """
        detalles = self.model.obtener_detalles_por_venta(id_venta)
        detalles_enriquecidos = []

        for detalle in detalles:
            codigo_articulo = detalle['codigo_articulo']
            articulo = self.articulo_model.obtener_articulo_por_codigo(codigo_articulo)

            if articulo:
                detalle_completo = {
                    "id_detalles_ventas": detalle['id_detalles_ventas'],
                    "codigo_articulo": codigo_articulo,
                    "nombre_articulo": articulo['nombre_articulo'],
                    "precio_unitario": float(articulo['precio']),
                    "cantidad": detalle['cantidad'],
                    "subtotal": round(float(articulo['precio']) * detalle['cantidad'], 2)
                }
                detalles_enriquecidos.append(detalle_completo)

        return detalles_enriquecidos

    def eliminar_detalle(self, id_detalles_ventas):
        """Permite eliminar un detalle individual de una venta."""
        return self.model.eliminar_detalle(id_detalles_ventas)
