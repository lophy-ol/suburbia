from views.vista_generica import crear_vista_generica
from controllers.controlador_caja import (
    cargar_cajas_en_treeview,
    guardar_caja,
    eliminar_caja_seleccionado,
    obtener_datos_de_seleccion
)

def crear_vista_caja(root, volver_callback):
    campos = [
        {"columna": "idcaja", "etiqueta": "ID", "clave": True},
        {"columna": "saldo_inicial", "etiqueta": "Saldo Inicial"},
        {"columna": "fecha_apertura", "etiqueta": "Fecha Apertura"},
        {"columna": "saldo_final", "etiqueta": "Saldo Final"},
        {"columna": "fecha_cierre", "etiqueta": "Fecha Cierre"}
    ]

    controlador = {
        "cargar": cargar_cajas_en_treeview,
        "guardar": guardar_caja,
        "eliminar": eliminar_caja_seleccionado,
        "obtener": obtener_datos_de_seleccion
    }

    return crear_vista_generica(root, "Caja", campos, controlador, volver_callback)
