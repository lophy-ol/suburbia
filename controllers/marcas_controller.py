from models.marcas_model import MarcasModel

class MarcasController:
    def __init__(self):
        self.model = MarcasModel()
    
    def obtener_marcas(self):
        return self.model.obtener_todas_marcas()
    
    def obtener_proveedores(self):
        return self.model.obtener_proveedores()
    
    def agregar_marca(self, nombre_marca, nombre_proveedor):
        proveedores = self.model.obtener_proveedores()
        proveedor_dict = {prov["nombre"]: prov["RFC"] for prov in proveedores}

        if nombre_proveedor not in proveedor_dict:
            raise Exception("Proveedor no válido")

        rfc = proveedor_dict[nombre_proveedor]
        try:
            return self.model.agregar_marca(nombre_marca, rfc)
        except Exception as e:
            raise Exception(f"Error al agregar marca: {e}")
    
    def actualizar_marca(self, id_marca, nombre_marca, nombre_proveedor):
        proveedores = self.model.obtener_proveedores()
        proveedor_dict = {prov["nombre"]: prov["RFC"] for prov in proveedores}
        
        if nombre_proveedor not in proveedor_dict:
            raise Exception("Proveedor no válido")
        
        rfc = proveedor_dict[nombre_proveedor]
        try:
            return self.model.actualizar_marca(id_marca, nombre_marca, rfc)
        except Exception as e:
            raise Exception(f"Error al actualizar marca: {e}")
    
    def eliminar_marca(self, id_marca):
        try:
            return self.model.eliminar_marca(id_marca)
        except Exception as e:
            raise Exception(f"Error al eliminar marca: {e}")