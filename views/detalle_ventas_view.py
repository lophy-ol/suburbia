import tkinter as tk
from tkinter import ttk
from controllers.detalle_ventas_controller import DetalleVentaController

class DetalleVentaView:
    def __init__(self, root):
        self.root = root
        self.root.title("Detalle de Ventas")
        self.root.geometry("950x400")
        self.controller = DetalleVentaController()

        self.crear_widgets()
        self.cargar_ventas()

    def crear_widgets(self):
        # Frame para ventas (izquierda)
        frame_ventas = ttk.LabelFrame(self.root, text="Ventas Realizadas")
        frame_ventas.pack(side="left", fill="y", padx=10, pady=10)

        self.tree_ventas = ttk.Treeview(frame_ventas, columns=("ID", "Total"), show="headings", height=15)
        self.tree_ventas.heading("ID", text="ID Venta")
        self.tree_ventas.heading("Total", text="Total ($)")
        self.tree_ventas.column("ID", width=80)
        self.tree_ventas.column("Total", width=100)
        self.tree_ventas.pack(padx=5, pady=5)

        self.tree_ventas.bind("<<TreeviewSelect>>", self.on_venta_select)

        # Frame para detalles (derecha)
        frame_detalles = ttk.LabelFrame(self.root, text="Detalles de la Venta")
        frame_detalles.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        columnas = ("ID Detalle", "Código", "Nombre", "Precio Unitario", "Cantidad", "Subtotal")
        self.tree_detalles = ttk.Treeview(frame_detalles, columns=columnas, show="headings", height=15)
        for col in columnas:
            self.tree_detalles.heading(col, text=col)
            self.tree_detalles.column(col, width=120)

        self.tree_detalles.pack(fill="both", expand=True, padx=5, pady=5)

    def cargar_ventas(self):
        ventas = self.controller.obtener_ventas()
        for venta in ventas:
            self.tree_ventas.insert("", "end", values=(venta["id_venta"], venta["total"]))

    def on_venta_select(self, event):
        selected_item = self.tree_ventas.selection()
        if selected_item:
            id_venta = self.tree_ventas.item(selected_item[0])["values"][0]
            detalles = self.controller.obtener_detalles_por_venta(id_venta)

            # Limpiar la tabla anterior
            for item in self.tree_detalles.get_children():
                self.tree_detalles.delete(item)

            for detalle in detalles:
                self.tree_detalles.insert("", "end", values=(
                    detalle["id_detalles_ventas"],
                    detalle["codigo_articulo"],
                    detalle["nombre_articulo"],
                    f"${detalle['precio_unitario']:.2f}",
                    detalle["cantidad"],
                    f"${detalle['subtotal']:.2f}"
                ))
