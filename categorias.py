import tkinter as tk
from views.categorias_view import CategoriasView

def main():
    root = tk.Tk()
    app = CategoriasView(root)
    root.mainloop()

if __name__ == "__main__":
    main()