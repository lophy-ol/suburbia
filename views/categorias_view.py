import tkinter as tk
from tkinter import ttk, messagebox
from controllers.categorias_controller import CategoriasController

class CategoriasView:
    def __init__(self, root):
        self.root = root
        self.controller = CategoriasController()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Gestión de Categorías")
        self.root.geometry("400x300")

        # Tabla de categorías
        self.tabla = ttk.Treeview(self.root, columns=("ID", "Tipo"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Tipo", text="Tipo de Categoría")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Formulario
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=5)

        self.input_id = tk.Entry(form_frame, state='disabled', width=10)
        self.input_tipo = tk.Entry(form_frame, width=25)

        self.input_id.insert(0, "ID (auto)")

        self.input_id.grid(row=0, column=0, padx=5)
        self.input_tipo.grid(row=0, column=1, padx=5)

        # Botones
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        btn_agregar = tk.Button(btn_frame, text="Agregar", command=self.agregar_categoria)
        btn_actualizar = tk.Button(btn_frame, text="Actualizar", command=self.actualizar_categoria)
        btn_eliminar = tk.Button(btn_frame, text="Eliminar", command=self.eliminar_categoria)

        btn_agregar.grid(row=0, column=0, padx=5)
        btn_actualizar.grid(row=0, column=1, padx=5)
        btn_eliminar.grid(row=0, column=2, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        try:
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)
            categorias = self.controller.obtener_categorias()
            for categoria in categorias:
                self.tabla.insert("", "end", values=(categoria["id_categorias"], categoria["tipo_categoria"] or ""))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla: {e}")

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.focus()
        if seleccionado:
            valores = self.tabla.item(seleccionado, "values")
            self.input_id.config(state="normal")
            self.input_id.delete(0, tk.END)
            self.input_id.insert(0, valores[0])
            self.input_id.config(state="disabled")
            self.input_tipo.delete(0, tk.END)
            self.input_tipo.insert(0, valores[1])

    def validar_campos(self):
        if not self.input_tipo.get().strip():
            messagebox.showwarning("Advertencia", "Ingrese el tipo de categoría.")
            return False
        return True

    def agregar_categoria(self):
        if not self.validar_campos():
            return
        try:
            self.controller.agregar_categoria(self.input_tipo.get().strip())
            messagebox.showinfo("Éxito", "Categoría agregada correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la categoría: {e}")

    def actualizar_categoria(self):
        if not self.validar_campos():
            return
        id_categoria = self.input_id.get().strip()
        if not id_categoria or id_categoria == "ID (auto)":
            messagebox.showwarning("Advertencia", "Seleccione una categoría de la tabla.")
            return
        try:
            self.controller.actualizar_categoria(id_categoria, self.input_tipo.get().strip())
            messagebox.showinfo("Éxito", "Categoría actualizada correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la categoría: {e}")

    def eliminar_categoria(self):
        id_categoria = self.input_id.get().strip()
        if not id_categoria or id_categoria == "ID (auto)":
            messagebox.showwarning("Advertencia", "Seleccione una categoría de la tabla.")
            return
        confirmacion = messagebox.askyesno("Confirmar eliminación",
                                       f"¿Está seguro de eliminar la categoría con ID '{id_categoria}'?")
        if confirmacion:
            try:
                self.controller.eliminar_categoria(id_categoria)
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente.")
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la categoría: {e}")

    def limpiar_campos(self):
        self.input_id.config(state="normal")
        self.input_id.delete(0, tk.END)
        self.input_id.insert(0, "ID (auto)")
        self.input_id.config(state="disabled")
        self.input_tipo.delete(0, tk.END)