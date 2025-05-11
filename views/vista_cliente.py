from views.vista_generica import crear_vista_generica
from controllers.controlador_cliente import (
    cargar_clientes_en_treeview,
    guardar_cliente,
    eliminar_cliente_seleccionado,
    obtener_datos_de_seleccion
)

def crear_vista_cliente(root, volver_callback):
    campos = [
        {"columna": "id_cliente", "etiqueta": "ID", "clave": True},
        {"columna": "nombre", "etiqueta": "Nombre"},
        {"columna": "apellido", "etiqueta": "Apellido"},
        {"columna": "telefono", "etiqueta": "Teléfono"},
        {"columna": "correo", "etiqueta": "Email"},
        {"columna": "direccion", "etiqueta": "Dirección"}
    ]

    controlador = {
        "cargar": cargar_clientes_en_treeview,
        "guardar": guardar_cliente,
        "eliminar": eliminar_cliente_seleccionado,
        "obtener": obtener_datos_de_seleccion
    }

    return crear_vista_generica(root, "Caja", campos, controlador, volver_callback)
