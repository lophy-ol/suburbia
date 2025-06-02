import tkinter as tk
from views.empleado_view import EmpleadoView

if __name__ == "__main__":
    root = tk.Tk()
    app = EmpleadoView(root)
    root.mainloop()