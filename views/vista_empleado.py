from views.vista_generica import crear_vista_generica
from controllers.controlador_empleado import (
    cargar_empleado_en_treeview,
    guardar_empleado,
    eliminar_empleado_seleccionado,
    obtener_datos_de_seleccion,
    obtener_ids_sucursal
)

def crear_vista_empleado(root, volver_callback):
    campos = [
        {"columna": "id_empleado", "etiqueta": "ID", "clave": True},
        {"columna": "nombre", "etiqueta": "Nombre"},
        {"columna": "apellido", "etiqueta": "Apellido"},
        {"columna": "cargo", "etiqueta": "Cargo"},
        {"columna": "fecha_contratacion", "etiqueta": "Fecha de Contratación"},
        {"columna": "salario", "etiqueta": "Salario"},
        {
            "columna": "id_sucursal",
            "etiqueta": "ID Sucursal",
            "tipo": "combobox",
            "opciones": obtener_ids_sucursal()
        }
    ]

    controlador = {
        "cargar": cargar_empleado_en_treeview,
        "guardar": guardar_empleado,
        "eliminar": eliminar_empleado_seleccionado,
        "obtener": obtener_datos_de_seleccion
    }

    return crear_vista_generica(root, "Empleados", campos, controlador, volver_callback)
