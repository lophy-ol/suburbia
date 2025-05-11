from views.vista_generica import crear_vista_generica
from controllers.controlador_sucursal import (
    cargar_sucursals_en_treeview,
    guardar_sucursal,
    eliminar_sucursal_seleccionado,
    obtener_datos_de_seleccion
)

def crear_vista_sucursal(root, volver_callback):
    campos = [
        {"columna": "id_sucursal", "etiqueta": "ID", "clave": True},
        {"columna": "nombre", "etiqueta": "Nombre"},
        {"columna": "direccion", "etiqueta": "Direccion"},
        {"columna": "ciudad", "etiqueta": "Ciudad"},
        {"columna": "estado", "etiqueta": "Estado"},
        {"columna": "codigo_postal", "etiqueta": "Codigo Postal"},
        {"columna": "telefono", "etiqueta": "Teléfono"}
    ]

    controlador = {
        "cargar": cargar_sucursals_en_treeview,
        "guardar": guardar_sucursal,
        "eliminar": eliminar_sucursal_seleccionado,
        "obtener": obtener_datos_de_seleccion
    }

    return crear_vista_generica(root, "Sucursal", campos, controlador, volver_callback)
