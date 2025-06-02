from models.articulo_model import ArticuloModel

class ArticuloController:
    def __init__(self):
        self.model = ArticuloModel()

    def obtener_categorias(self):
        return self.model.obtener_categorias()

    def obtener_marcas(self):
        return self.model.obtener_marcas()

    def obtener_articulos(self):
        return self.model.obtener_articulos()

    def agregar_articulo(self, codigo_articulo, nombre_articulo, activado, precio, stock, gasto, categoria, marca):
        try:
            # Validaciones básicas
            if not codigo_articulo or not nombre_articulo:
                return False, "Código y nombre son campos obligatorios"
            
            self.model.agregar_articulo(codigo_articulo, nombre_articulo, activado, 
                                    precio, stock, gasto, categoria, marca)
            return True, "Artículo agregado correctamente."
        except Exception as e:
            return False, str(e)

    def actualizar_articulo(self, codigo, nombre, activado, precio, stock, gasto, categoria, marca):
        try:
            self.model.actualizar_articulo(codigo, nombre, activado, precio, 
                                        stock, gasto, categoria, marca)
            return True, "Artículo actualizado correctamente."
        except Exception as e:
            return False, f"No se pudo actualizar el artículo:\n{e}"

    def eliminar_articulo(self, codigo):
        try:
            self.model.eliminar_articulo(codigo)
            return True, "Artículo eliminado correctamente."
        except Exception as e:
            return False, f"No se pudo eliminar el artículo:\n{e}"
