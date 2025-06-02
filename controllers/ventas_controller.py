from models.ventas_model import VentasModel
from models.cliente_model import ClienteModel
from models.empleado_model import EmpleadoModel
from models.metodo_pago_model import MetodoPagoModel
from models.articulo_model import ArticuloModel
    
class VentasController:
    def __init__(self):
        self.model = VentasModel()
        self.cliente_model = ClienteModel()
        self.empleado_model = EmpleadoModel()
        self.metodo_pago_model = MetodoPagoModel()
        self.articulo_model = ArticuloModel()

    def obtener_ventas(self):
        return self.model.obtener_ventas()

    def obtener_clientes(self):
        # Retorna clientes para toggle (usualmente particulares)
        return self.cliente_model.obtener_todos()

    def obtener_empleados(self):
        # Retorna empleados para toggle
        return self.empleado_model.obtener_todos()

    def obtener_metodos_pago(self):
        # Retorna métodos de pago para toggle
        return self.metodo_pago_model.obtener_metodos_pago()

    def obtener_articulo_por_codigo(self, codigo):
        return self.articulo_model.obtener_articulo_por_codigo(codigo)


    def agregar_venta(self, id_venta, total, id_cliente, id_empleado, tipo_cliente,
                      codigo_articulo, cantidad, id_modo_pago, nombre_articulo):
        # Si el tipo de cliente es "General", forzar id_cliente = 4
        if tipo_cliente.lower() == "general":
            id_cliente = 4

        # Validar que total esté calculado correctamente (podría hacerse aquí o en vista)
        # Pero para seguridad, recalculamos total con IVA:
        articulo = self.obtener_articulo_por_codigo(codigo_articulo)
        if articulo is None:
            print("Error: artículo no encontrado.")
            return False
        
        try:
            precio = float(articulo["precio"])  # Asumiendo que el campo es 'precio'
            cantidad = int(cantidad)
            total_calculado = round(precio * cantidad * 1.16, 2)  # IVA 16%
            if abs(float(total) - total_calculado) > 0.01:
                total = total_calculado  # Corrige total si está mal enviado
        except Exception as e:
            print(f"Error en cálculo de total: {e}")
            return False

        return self.model.agregar_venta(
            id_venta, total, id_cliente, id_empleado, tipo_cliente,
            codigo_articulo, cantidad, id_modo_pago, nombre_articulo
        )

    def actualizar_venta(self, id_venta, total, id_cliente, id_empleado, tipo_cliente,
                         codigo_articulo, cantidad, id_modo_pago, nombre_articulo):
        # Similar lógica para actualizar
        if tipo_cliente.lower() == "general":
            id_cliente = 4

        articulo = self.obtener_articulo_por_codigo(codigo_articulo)
        if articulo is None:
            print("Error: artículo no encontrado.")
            return False
        
        try:
            precio = float(articulo["precio"])
            cantidad = int(cantidad)
            total_calculado = round(precio * cantidad * 1.16, 2)
            if abs(float(total) - total_calculado) > 0.01:
                total = total_calculado
        except Exception as e:
            print(f"Error en cálculo de total: {e}")
            return False

        return self.model.actualizar_venta(
            id_venta, total, id_cliente, id_empleado, tipo_cliente,
            codigo_articulo, cantidad, id_modo_pago, nombre_articulo
        )

    def eliminar_venta(self, id_venta):
        return self.model.eliminar_venta(id_venta)
