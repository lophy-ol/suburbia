# import tkinter as tk
# from tkinter import ttk
# from controllers.controlador_proveedor import (
#     cargar_proveedores_en_treeview,
#     guardar_proveedor,
#     eliminar_proveedor_seleccionado,
#     obtener_datos_de_seleccion
# )

# def crear_vista_proveedor(root, volver_callback):
#     frame = ttk.Frame(root)

#     # Parte superior
#     top_frame = ttk.Frame(frame)
#     top_frame.pack(fill=tk.X, pady=5)

#     ttk.Button(top_frame, text="Volver", command=volver_callback).pack(side=tk.LEFT, padx=5)
#     ttk.Button(top_frame, text="Agregar Proveedor", command=lambda: abrir_dialogo_proveedor(frame)).pack(side=tk.LEFT, padx=5)

#     # Tabla
#     columnas = ['ID', 'Nombre', 'Teléfono', 'Correo', 'Dirección']
#     tree = ttk.Treeview(frame, columns=columnas, show='headings')
#     tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

#     for col in columnas:
#         tree.heading(col, text=col, anchor=tk.CENTER)
#         tree.column(col, width=140, anchor=tk.CENTER)

#     scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
#     tree.configure(yscroll=scrollbar.set)
#     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#     tree.bind('<Double-1>', lambda event: editar_proveedor(tree, frame))

#     # Botones inferiores
#     btn_frame = ttk.Frame(frame)
#     btn_frame.pack(fill=tk.X, pady=5)

#     ttk.Button(btn_frame, text="Editar", command=lambda: editar_proveedor(tree, frame)).pack(side=tk.LEFT, padx=5)
#     ttk.Button(btn_frame, text="Eliminar", command=lambda: eliminar_proveedor_seleccionado(tree)).pack(side=tk.LEFT, padx=5)

#     # Cargar proveedores en la tabla
#     cargar_proveedores_en_treeview(tree)

#     # Empaquetar el frame principal
#     frame.pack(fill=tk.BOTH, expand=True)

#     return frame

# def abrir_dialogo_proveedor(parent, proveedor=None):
#     dialog = tk.Toplevel(parent)
#     dialog.title("Editar Proveedor" if proveedor else "Agregar Proveedor")
#     dialog.grab_set()

#     labels = ["ID", "Nombre", "Telefono", "Correo", "Direccion"]
#     entries = {}

#     for i, label in enumerate(labels):
#         ttk.Label(dialog, text=label + ":").grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
#         entry = ttk.Entry(dialog, width=30)
#         entry.grid(row=i, column=1, padx=5, pady=5)
#         entries[label.lower()] = entry

#     if proveedor:
#         entries["id"].insert(0, proveedor[0])
#         entries["id"].config(state='readonly')
#         for i, key in enumerate(["nombre", "telefono", "correo", "direccion"]):
#             entries[key].insert(0, proveedor[i+1])

#     btn_frame = ttk.Frame(dialog)
#     btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

#     ttk.Button(btn_frame, text="Guardar", command=lambda: guardar_proveedor(
#         {k: e.get().strip() for k, e in entries.items()},
#         parent.children['!treeview'],
#         dialog,
#         proveedor is not None
#     )).pack(side=tk.LEFT, padx=5)

#     ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

# def editar_proveedor(tree, parent):
#     proveedor = obtener_datos_de_seleccion(tree)
#     if proveedor:
#         abrir_dialogo_proveedor(parent, proveedor)


from views.vista_generica import crear_vista_generica
from controllers.controlador_proveedor import (
    cargar_proveedores_en_treeview,
    guardar_proveedor,
    eliminar_proveedor_seleccionado,
    obtener_datos_de_seleccion
)

def crear_vista_proveedor(root, volver_callback):
    campos = [
        {"columna": "id_proveedor", "etiqueta": "ID", "clave": True},
        {"columna": "nombre", "etiqueta": "Nombre"},
        {"columna": "telefono", "etiqueta": "Teléfono"},
        {"columna": "correo", "etiqueta": "Correo"},
        {"columna": "direccion", "etiqueta": "Dirección"}
    ]

    controlador = {
        "cargar": cargar_proveedores_en_treeview,
        "guardar": guardar_proveedor,
        "eliminar": eliminar_proveedor_seleccionado,
        "obtener": obtener_datos_de_seleccion
    }

    return crear_vista_generica(root, "Proveedor", campos, controlador, volver_callback)
