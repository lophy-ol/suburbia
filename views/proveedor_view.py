import tkinter as tk
from tkinter import ttk, messagebox
from controllers.proveedor_controller import ProveedorController

class ProveedorView:
    def __init__(self, root):
        self.root = root
        self.controller = ProveedorController()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Gestión de Proveedores")
        self.root.geometry("800x400")

        # Tabla
        self.tabla = ttk.Treeview(self.root, columns=("RFC", "Nombre", "Teléfono", "Correo", "Dirección"), show='headings')
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=10)

        # Formulario
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        self.input_RFC = tk.Entry(form_frame)
        self.input_nombre = tk.Entry(form_frame)
        self.input_telefono = tk.Entry(form_frame)
        self.input_correo = tk.Entry(form_frame)
        self.input_direccion = tk.Entry(form_frame)

        for idx, (label, entry) in enumerate(zip(["RFC", "Nombre", "Teléfono", "Correo", "Dirección"],
                                                [self.input_RFC, self.input_nombre, self.input_telefono, self.input_correo, self.input_direccion])):
            tk.Label(form_frame, text=label).grid(row=0, column=idx)
            entry.grid(row=1, column=idx, padx=5)

        # Botones
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Agregar", command=self.agregar_proveedor).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Actualizar", command=self.actualizar_proveedor).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_proveedor).pack(side=tk.LEFT, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        try:
            proveedores = self.controller.obtener_proveedores()
            for i in self.tabla.get_children():
                self.tabla.delete(i)
            for proveedor in proveedores:
                self.tabla.insert('', tk.END, values=(
                    proveedor["RFC"],
                    proveedor["nombre"] or "",
                    proveedor["telefono"] or "",
                    proveedor["correo"] or "",
                    proveedor["direccion"] or ""
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla: {e}")

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.selection()
        if seleccionado:
            valores = self.tabla.item(seleccionado[0], "values")
            self.limpiar_campos()
            
            self.input_RFC.insert(0, valores[0])
            self.input_nombre.insert(0, valores[1])
            self.input_telefono.insert(0, valores[2])
            self.input_correo.insert(0, valores[3])
            self.input_direccion.insert(0, valores[4])

    def validar_campos(self):
        if not all([
            self.input_RFC.get().strip(),
            self.input_nombre.get().strip(),
            self.input_telefono.get().strip(),
            self.input_correo.get().strip(),
            self.input_direccion.get().strip()
        ]):
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
            return False
        return True

    def agregar_proveedor(self):
        if not self.validar_campos():
            return
        datos = (
            self.input_RFC.get().strip(),
            self.input_nombre.get().strip(),
            self.input_telefono.get().strip(),
            self.input_correo.get().strip(),
            self.input_direccion.get().strip()
        )
        if self.controller.agregar_proveedor(*datos):
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo agregar el proveedor.")

    def actualizar_proveedor(self):
        if not self.validar_campos():
            return
        datos = (
            self.input_RFC.get().strip(),
            self.input_nombre.get().strip(),
            self.input_telefono.get().strip(),
            self.input_correo.get().strip(),
            self.input_direccion.get().strip()
        )
        if self.controller.actualizar_proveedor(*datos):
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el proveedor.")

    def eliminar_proveedor(self):
        rfc = self.input_RFC.get().strip()
        if not rfc:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor de la tabla.")
            return
        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el proveedor con RFC '{rfc}'?")
        if confirmacion and self.controller.eliminar_proveedor(rfc):
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        elif confirmacion:
            messagebox.showerror("Error", "No se pudo eliminar el proveedor.")

    def limpiar_campos(self):
        self.input_RFC.delete(0, tk.END)
        self.input_nombre.delete(0, tk.END)
        self.input_telefono.delete(0, tk.END)
        self.input_correo.delete(0, tk.END)
        self.input_direccion.delete(0, tk.END)
 