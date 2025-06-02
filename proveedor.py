import tkinter as tk
from views.proveedor_view import ProveedorView

if __name__ == "__main__":
    root = tk.Tk()
    app = ProveedorView(root)
    root.mainloop()