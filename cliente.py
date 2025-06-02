from views.cliente_view import ClienteView
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteView(root)
    root.mainloop()