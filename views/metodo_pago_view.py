import tkinter as tk
from tkinter import ttk, messagebox
from controllers.metodo_pago_controller import MetodoPagoController
#sgsfhs

class MetodoPagoView:
    def __init__(self, root):
        self.root = root
        self.controller = MetodoPagoController()
        self.id_seleccionado = None

        self.configurar_ventana()
        self.crear_widgets()
        self.cargar_metodos_pago()

    def configurar_ventana(self):
        self.root.title("Gestión de Métodos de Pago")
        self.root.geometry("600x400")

    def crear_widgets(self):
        frame_form = tk.Frame(self.root)
        frame_form.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(frame_form, text="Tipo de pago:").grid(row=0, column=0, sticky=tk.W)
        self.input_tipo = tk.Entry(frame_form)
        self.input_tipo.grid(row=0, column=1)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(padx=10, pady=10)

        tk.Button(frame_botones, text="Agregar", command=self.agregar_metodo).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Actualizar", command=self.actualizar_metodo).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar_metodo).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=3, padx=5)

        self.tabla = ttk.Treeview(self.root, columns=("id", "tipo"), show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.column("id", width=50, anchor=tk.CENTER)
        self.tabla.column("tipo", anchor=tk.CENTER)
        self.tabla.pack(fill=tk.BOTH, expand=True)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)

    def cargar_metodos_pago(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        metodos = self.controller.obtener_metodos_pago()
        for metodo in metodos:
            self.tabla.insert("", tk.END, values=(metodo["id_modo_pago"], metodo["tipo"]))

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.focus()
        if seleccionado:
            valores = self.tabla.item(seleccionado)["values"]
            self.id_seleccionado = valores[0]
            self.input_tipo.delete(0, tk.END)
            self.input_tipo.insert(0, valores[1])
        else:
            self.id_seleccionado = None

    def agregar_metodo(self):
        tipo = self.input_tipo.get().strip()
        if not tipo:
            messagebox.showerror("Error", "El tipo de método de pago no puede estar vacío.")
            return

        exito, mensaje = self.controller.agregar_metodo_pago(tipo)
        if exito:
            self.cargar_metodos_pago()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    def actualizar_metodo(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Selección requerida", "Selecciona un método de pago para actualizar.")
            return

        nuevo_tipo = self.input_tipo.get().strip()
        if not nuevo_tipo:
            messagebox.showerror("Error", "El nuevo tipo no puede estar vacío.")
            return

        exito, mensaje = self.controller.actualizar_metodo_pago(self.id_seleccionado, nuevo_tipo)
        if exito:
            self.cargar_metodos_pago()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_metodo(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Selección requerida", "Selecciona un método de pago para eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este método de pago?")
        if respuesta:
            exito, mensaje = self.controller.eliminar_metodo_pago(self.id_seleccionado)
            if exito:
                self.cargar_metodos_pago()
                self.limpiar_campos()
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showerror("Error", mensaje)

    def limpiar_campos(self):
        self.id_seleccionado = None
        self.input_tipo.delete(0, tk.END)
