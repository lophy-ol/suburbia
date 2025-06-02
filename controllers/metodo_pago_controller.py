from models.metodo_pago_model import MetodoPagoModel

class MetodoPagoController:
    def __init__(self):
        self.model = MetodoPagoModel()

    def obtener_metodos_pago(self):
        return self.model.obtener_metodos_pago()

    def agregar_metodo_pago(self, tipo):
        try:
            if not tipo or not tipo.strip():
                return False, "El tipo de método de pago no puede estar vacío."
            
            self.model.agregar_metodo_pago(tipo)
            return True, "Método de pago agregado correctamente."
        except Exception as e:
            return False, f"No se pudo agregar el método de pago:\n{e}"

    def actualizar_metodo_pago(self, id_modo_pago, nuevo_tipo):
        try:
            if not nuevo_tipo or not nuevo_tipo.strip():
                return False, "El nuevo tipo no puede estar vacío."
            
            self.model.actualizar_metodo_pago(id_modo_pago, nuevo_tipo)
            return True, "Método de pago actualizado correctamente."
        except Exception as e:
            return False, f"No se pudo actualizar el método de pago:\n{e}"

    def eliminar_metodo_pago(self, id_modo_pago):
        try:
            self.model.eliminar_metodo_pago(id_modo_pago)
            return True, "Método de pago eliminado correctamente."
        except Exception as e:
            return False, f"No se pudo eliminar el método de pago:\n{e}"
