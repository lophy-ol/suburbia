from views.vista_generica import crear_vista_generica
from controllers.controlador_metodo_pago import (
    cargar_metodo_pago_en_treeview,
    guardar_metodo_pago,
    eliminar_metodo_pago_seleccionado,
    obtener_datos_de_seleccion
)

def crear_vista_metodo_pago(root, volver_callback):
    campos = [
        {"columna": "idmetodo_pago", "etiqueta": "ID", "clave": True},
        {"columna": "nombre", "etiqueta": "Nombre"},
        {"columna": "descripcion", "etiqueta": "Descripcion"},
        {
            "columna": "activo",
            "etiqueta": "Activo",
            "tipo": "combobox",
            "opciones": ["Si", "No"]
        }
    ]

    controlador = {
        "cargar": cargar_metodo_pago_en_treeview,
        "guardar": guardar_metodo_pago,
        "eliminar": eliminar_metodo_pago_seleccionado,
        "obtener": obtener_datos_de_seleccion
    }

    return crear_vista_generica(root, "Método de Pago", campos, controlador, volver_callback)
