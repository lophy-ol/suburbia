from models.sucursal_model import SucursalModel

class SucursalController:
    def __init__(self):
        self.model = SucursalModel()

    def obtener_sucursales(self):
        return self.model.obtener_todas()

    def agregar_sucursal(self, datos_sucursal):
        return self.model.agregar(**datos_sucursal)

    def actualizar_sucursal(self, id_sucursal, datos_sucursal):
        return self.model.actualizar(id_sucursal, **datos_sucursal)

    def eliminar_sucursal(self, id_sucursal):
        return self.model.eliminar(id_sucursal)