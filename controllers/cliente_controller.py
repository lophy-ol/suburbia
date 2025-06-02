from models.cliente_model import ClienteModel

class ClienteController:
    @staticmethod
    def obtener_clientes():
        return ClienteModel.obtener_todos()

    @staticmethod
    def agregar_cliente(nombre, apellido, telefono, correo, direccion):
        return ClienteModel.agregar_cliente(nombre, apellido, telefono, correo, direccion)

    @staticmethod
    def actualizar_cliente(id_cliente, nombre, apellido, telefono, correo, direccion):
        return ClienteModel.actualizar_cliente(id_cliente, nombre, apellido, telefono, correo, direccion)

    @staticmethod
    def eliminar_cliente(id_cliente):
        return ClienteModel.eliminar_cliente(id_cliente)