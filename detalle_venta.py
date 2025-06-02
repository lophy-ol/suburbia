import tkinter as tk
from views.detalle_ventas_view import DetalleVentaView

if __name__ == "__main__":
    root = tk.Tk()
    app = DetalleVentaView(root)
    root.mainloop()