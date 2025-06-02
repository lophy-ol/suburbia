from models.categorias_model import CategoriasModel

class CategoriasController:
    def __init__(self):
        self.model = CategoriasModel()

    def obtener_categorias(self):
        return self.model.obtener_todas()

    def agregar_categoria(self, tipo_categoria):
        return self.model.agregar(tipo_categoria)

    def actualizar_categoria(self, id_categoria, tipo_categoria):
        return self.model.actualizar(id_categoria, tipo_categoria)

    def eliminar_categoria(self, id_categoria):
        return self.model.eliminar(id_categoria)