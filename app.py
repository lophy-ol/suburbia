import tkinter as tk
from tkinter import ttk
from views.ventas_view import VentasView
from views.detalle_ventas_view import DetalleVentaView
from views.articulo_view import ArticuloView
from views.cliente_view import ClienteView
from views.empleado_view import EmpleadoView
from views.metodo_pago_view import MetodoPagoView
from views.proveedor_view import ProveedorView
from views.sucursal_view import SucursalView
from views.categorias_view import CategoriasView
from views.marcas_view import VentanaMarcas

class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Suburbia")
        self.root.geometry("400x500")
        self.root.configure(bg="#f5f5f5")
        
        # Esta línea evita que se cree una ventana Tk adicional
        self.root.withdraw()  # Oculta la ventana principal temporalmente
        
        self.crear_interfaz()
        
        # Vuelve a mostrar la ventana principal después de configurarla
        self.root.deiconify()

    def crear_interfaz(self):
        label = tk.Label(self.root, text="Menú Principal", font=("Arial", 18), bg="#f5f5f5")
        label.pack(pady=20)

        botones = [
            ("Ventas", VentasView),
            ("Detalle Ventas", DetalleVentaView),
            ("Artículos", ArticuloView),
            ("Clientes", ClienteView),
            ("Empleados", EmpleadoView),
            ("Métodos de Pago", MetodoPagoView),
            ("Proveedores", ProveedorView),
            ("Sucursales", SucursalView),
            ("Categorías", CategoriasView),
            ("Marcas", VentanaMarcas)
        ]

        for texto, clase_vista in botones:
            btn = ttk.Button(self.root, text=texto, width=25, 
                           command=lambda vista=clase_vista: self.abrir_ventana(vista))
            btn.pack(pady=5)

    def abrir_ventana(self, VistaClase):
        # Verificar si es la ventana de Marcas para manejo especial
        if VistaClase.__name__ == "VentanaMarcas":
            # Destruir cualquier ventana Tk existente
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
        
        nueva_ventana = tk.Toplevel(self.root)
        nueva_ventana.transient(self.root)
        nueva_ventana.grab_set()
        VistaClase(nueva_ventana)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppPrincipal(root)
    root.mainloop()