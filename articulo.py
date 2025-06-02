import tkinter as tk
from views.articulo_view import ArticuloView

if __name__ == "__main__":
    root = tk.Tk()
    app = ArticuloView(root)
    root.mainloop()