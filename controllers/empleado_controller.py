from models.empleado_model import EmpleadoModel

class EmpleadoController:
    @staticmethod
    def obtener_empleados():
        return EmpleadoModel.obtener_todos()

    @staticmethod
    def agregar_empleado(nombre, apellido, cargo, fecha, salario, id_sucursal):
        EmpleadoModel.agregar(nombre, apellido, cargo, fecha, salario, id_sucursal)

    @staticmethod
    def actualizar_empleado(id_empleado, nombre, apellido, cargo, fecha, salario, id_sucursal):
        EmpleadoModel.actualizar(id_empleado, nombre, apellido, cargo, fecha, salario, id_sucursal)

    @staticmethod
    def eliminar_empleado(id_empleado):
        EmpleadoModel.eliminar(id_empleado)

    @staticmethod
    def obtener_sucursales():
        return EmpleadoModel.obtener_sucursales()