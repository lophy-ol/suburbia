from views.vista_generica import crear_vista_generica
from controllers.controlador_almacen import (
    cargar_almacens_en_treeview,
    guardar_almacen,
    eliminar_almacen_seleccionado,
    obtener_datos_de_seleccion
)

def crear_vista_almacen(root, volver_callback):
    campos = [
        {"columna": "idalmacen", "etiqueta": "ID", "clave": True},
        {"columna": "nombre", "etiqueta": "Nombre"},
        {"columna": "ubicacion", "etiqueta": "Ubicación"},
        {"columna": "capacidad_maxima", "etiqueta": "Capacidad Maxima"},
        {
            "columna": "estado",
            "etiqueta": "Estado",
            "tipo": "combobox",
            "opciones": ["Activo", "Inactivo"]
        }
    ]

    controlador = {
        "cargar": cargar_almacens_en_treeview,
        "guardar": guardar_almacen,
        "eliminar": eliminar_almacen_seleccionado,
        "obtener": obtener_datos_de_seleccion
    }

    return crear_vista_generica(root, "Almacen", campos, controlador, volver_callback)
