import tkinter as tk
from tkinter import ttk, messagebox
from controllers.sucursal_controller import SucursalController

class SucursalView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Sucursales - Suburbia")
        self.geometry("800x600")
        self.controller = SucursalController()
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        # Tabla de sucursales
        self.tabla = ttk.Treeview(self, columns=(
            "ID", "Nombre", "Dirección", "Ciudad", "Estado", "CP", "Teléfono"), show="headings")
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Formulario
        form_frame = tk.Frame(self)
        form_frame.pack(pady=5)

        self.inputs = {}
        labels = ["ID (auto)", "Nombre", "Dirección", "Ciudad", "Estado", "Código Postal", "Teléfono"]
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2)
            if i == 0:  # ID
                entry.config(state="disabled")
            self.inputs[label] = entry

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        btn_agregar = tk.Button(btn_frame, text="Agregar", command=self.agregar_sucursal)
        btn_actualizar = tk.Button(btn_frame, text="Actualizar", command=self.actualizar_sucursal)
        btn_eliminar = tk.Button(btn_frame, text="Eliminar", command=self.eliminar_sucursal)

        btn_agregar.grid(row=0, column=0, padx=5)
        btn_actualizar.grid(row=0, column=1, padx=5)
        btn_eliminar.grid(row=0, column=2, padx=5)

    def cargar_datos(self):
        try:
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)
            sucursales = self.controller.obtener_sucursales()
            for sucursal in sucursales:
                self.tabla.insert("", "end", values=(
                    sucursal["id_sucursal"], sucursal["nombre"], sucursal["direccion"],
                    sucursal["ciudad"], sucursal["estado"], sucursal["codigo_postal"], sucursal["telefono"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla: {e}")

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.focus()
        if seleccionado:
            valores = self.tabla.item(seleccionado, "values")
            campos = ["ID (auto)", "Nombre", "Dirección", "Ciudad", "Estado", "Código Postal", "Teléfono"]
            for i, campo in enumerate(campos):
                entry = self.inputs[campo]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, valores[i])
                if campo == "ID (auto)":
                    entry.config(state="disabled")

    def validar_campos(self):
        campos_obligatorios = ["Nombre", "Dirección", "Ciudad", "Estado", "Código Postal", "Teléfono"]
        for campo in campos_obligatorios:
            if not self.inputs[campo].get().strip():
                messagebox.showwarning("Advertencia", f"Ingrese {campo}.")
                return False
        return True

    def agregar_sucursal(self):
        if not self.validar_campos():
            return
        try:
            datos = {
                "nombre": self.inputs["Nombre"].get().strip(),
                "direccion": self.inputs["Dirección"].get().strip(),
                "ciudad": self.inputs["Ciudad"].get().strip(),
                "estado": self.inputs["Estado"].get().strip(),
                "codigo_postal": self.inputs["Código Postal"].get().strip(),
                "telefono": self.inputs["Teléfono"].get().strip()
            }
            self.controller.agregar_sucursal(datos)
            messagebox.showinfo("Éxito", "Sucursal agregada correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la sucursal: {e}")

    def actualizar_sucursal(self):
        if not self.validar_campos():
            return
        id_sucursal = self.inputs["ID (auto)"].get().strip()
        if not id_sucursal:
            messagebox.showwarning("Advertencia", "Seleccione una sucursal de la tabla.")
            return
        try:
            datos = {
                "nombre": self.inputs["Nombre"].get().strip(),
                "direccion": self.inputs["Dirección"].get().strip(),
                "ciudad": self.inputs["Ciudad"].get().strip(),
                "estado": self.inputs["Estado"].get().strip(),
                "codigo_postal": self.inputs["Código Postal"].get().strip(),
                "telefono": self.inputs["Teléfono"].get().strip()
            }
            self.controller.actualizar_sucursal(id_sucursal, datos)
            messagebox.showinfo("Éxito", "Sucursal actualizada correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la sucursal: {e}")

    def eliminar_sucursal(self):
        id_sucursal = self.inputs["ID (auto)"].get().strip()
        if not id_sucursal:
            messagebox.showwarning("Advertencia", "Seleccione una sucursal de la tabla.")
            return
        confirmacion = messagebox.askyesno("Confirmar eliminación",
                                       f"¿Está seguro de eliminar la sucursal con ID '{id_sucursal}'?")
        if confirmacion:
            try:
                self.controller.eliminar_sucursal(id_sucursal)
                messagebox.showinfo("Éxito", "Sucursal eliminada correctamente.")
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la sucursal: {e}")

    def limpiar_campos(self):
        for campo, entry in self.inputs.items():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            if campo == "ID (auto)":
                entry.insert(0, "")
                entry.config(state="disabled")

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    app = SucursalView()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()