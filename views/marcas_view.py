import tkinter as tk
from tkinter import ttk, messagebox
from controllers.marcas_controller import MarcasController


class VentanaMarcas(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Marcas")
        self.geometry("600x400")
        self.id_marca_seleccionada = None
        self.controller = MarcasController()

        self.crear_widgets()
        self.cargar_proveedores()
        self.cargar_datos()

    def crear_widgets(self):
        # Tabla
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Proveedor"), show="headings")
        self.tabla.heading("ID", text="ID Marca")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Proveedor", text="Proveedor")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=5)

        # Formulario
        form_frame = tk.Frame(self)
        form_frame.pack(pady=5)

        self.input_nombre = tk.Entry(form_frame)
        self.input_nombre.pack(side=tk.LEFT, padx=5)
        self.input_nombre.insert(0, "Nombre de la Marca")

        self.combo_proveedor = ttk.Combobox(form_frame, state="readonly")
        self.combo_proveedor.pack(side=tk.LEFT, padx=5)

        # Botones
        botones_frame = tk.Frame(self)
        botones_frame.pack(pady=10)

        btn_agregar = tk.Button(botones_frame, text="Agregar", command=self.agregar_marca)
        btn_actualizar = tk.Button(botones_frame, text="Actualizar", command=self.actualizar_marca)
        btn_eliminar = tk.Button(botones_frame, text="Eliminar", command=self.eliminar_marca)

        btn_agregar.pack(side=tk.LEFT, padx=5)
        btn_actualizar.pack(side=tk.LEFT, padx=5)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

    def cargar_proveedores(self):
        try:
            proveedores = self.controller.obtener_proveedores()
            self.proveedor_dict = {prov["nombre"]: prov["RFC"] for prov in proveedores}
            self.combo_proveedor["values"] = list(self.proveedor_dict.keys())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores: {e}")

    def cargar_datos(self):
        try:
            resultados = self.controller.obtener_marcas()
            self.tabla.delete(*self.tabla.get_children())
            for marca in resultados:
                self.tabla.insert("", tk.END, values=(
                    marca["id_marca"],
                    marca["nombre_marca"],
                    marca["nombre"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla: {e}")

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion[0])["values"]
            self.id_marca_seleccionada = valores[0]
            self.input_nombre.delete(0, tk.END)
            self.input_nombre.insert(0, valores[1])
            self.combo_proveedor.set(valores[2])

    def validar_campos(self):
        nombre = self.input_nombre.get().strip()
        proveedor = self.combo_proveedor.get()
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre de la marca no puede estar vacío.")
            return False
        if proveedor not in self.proveedor_dict:
            messagebox.showwarning("Advertencia", "Debe seleccionar un proveedor.")
            return False
        return True

    def agregar_marca(self):
        if not self.validar_campos():
            return
        try:
            nombre = self.input_nombre.get().strip()
            proveedor = self.combo_proveedor.get()
            self.controller.agregar_marca(nombre, proveedor)
            messagebox.showinfo("Éxito", "Marca agregada correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la marca: {e}")

    def actualizar_marca(self):
        if not self.validar_campos() or self.id_marca_seleccionada is None:
            messagebox.showwarning("Advertencia", "Seleccione una marca de la tabla para actualizar.")
            return
        try:
            nombre = self.input_nombre.get().strip()
            proveedor = self.combo_proveedor.get()
            self.controller.actualizar_marca(self.id_marca_seleccionada, nombre, proveedor)
            messagebox.showinfo("Éxito", "Marca actualizada correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la marca: {e}")

    def eliminar_marca(self):
        if self.id_marca_seleccionada is None:
            messagebox.showwarning("Advertencia", "Seleccione una marca para eliminar.")
            return
        confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de eliminar esta marca?")
        if confirmacion:
            try:
                self.controller.eliminar_marca(self.id_marca_seleccionada)
                messagebox.showinfo("Éxito", "Marca eliminada correctamente.")
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la marca: {e}")

    def limpiar_campos(self):
        self.input_nombre.delete(0, tk.END)
        self.combo_proveedor.set("")
        self.id_marca_seleccionada = None