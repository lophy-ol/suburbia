import tkinter as tk
from tkinter import ttk, messagebox
from controllers.empleado_controller import EmpleadoController

class EmpleadoView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Empleados")
        self.root.geometry("1600x400")
        self.sucursales = {}
        self.crear_widgets()
        self.cargar_datos()
        self.cargar_sucursales()

    def crear_widgets(self):
        # Tabla
        self.tabla = ttk.Treeview(self.root, columns=("ID", "Nombre", "Apellido", "Cargo", "Fecha", "Salario", "Sucursal"), show="headings")
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Formulario
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=5)

        self.input_id = tk.Entry(form_frame, state='disabled', width=5)
        self.input_nombre = tk.Entry(form_frame, width=15)
        self.input_apellido = tk.Entry(form_frame, width=15)
        self.input_cargo = tk.Entry(form_frame, width=15)
        self.input_fecha = tk.Entry(form_frame, width=10)  # YYYY-MM-DD
        self.input_salario = tk.Entry(form_frame, width=10)
        self.combo_sucursal = ttk.Combobox(form_frame, width=15, state='readonly')

        self.input_id.insert(0, "ID (auto)")
        self.input_id.grid(row=0, column=0, padx=5)
        self.input_nombre.grid(row=0, column=1, padx=5)
        self.input_apellido.grid(row=0, column=2, padx=5)
        self.input_cargo.grid(row=0, column=3, padx=5)
        self.input_fecha.grid(row=0, column=4, padx=5)
        self.input_salario.grid(row=0, column=5, padx=5)
        self.combo_sucursal.grid(row=0, column=6, padx=5)

        # Botones
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Agregar", command=self.agregar_empleado).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Actualizar", command=self.actualizar_empleado).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_empleado).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Recargar Sucursales", command=self.cargar_sucursales).grid(row=0, column=3, padx=5)

    def cargar_datos(self):
        try:
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)
            empleados = EmpleadoController.obtener_empleados()
            for fila in empleados:
                self.tabla.insert("", "end", values=(
                    fila["id_empleado"], fila["Nombre"], fila["Apellido"], fila["Cargo"],
                    fila["Fecha_Contratacion"], fila["Salario"], fila["sucursal"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla: {e}")

    def cargar_sucursales(self):
        try:
            sucursales = EmpleadoController.obtener_sucursales()
            self.sucursales = {s["nombre"]: s["id_sucursal"] for s in sucursales}
            self.combo_sucursal['values'] = list(self.sucursales.keys())
            self.combo_sucursal.set("")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las sucursales: {e}")

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.focus()
        if seleccionado:
            valores = self.tabla.item(seleccionado, "values")
            self.input_id.config(state="normal")
            self.input_id.delete(0, tk.END)
            self.input_id.insert(0, valores[0])
            self.input_id.config(state="disabled")
            self.input_nombre.delete(0, tk.END)
            self.input_nombre.insert(0, valores[1])
            self.input_apellido.delete(0, tk.END)
            self.input_apellido.insert(0, valores[2])
            self.input_cargo.delete(0, tk.END)
            self.input_cargo.insert(0, valores[3])
            self.input_fecha.delete(0, tk.END)
            self.input_fecha.insert(0, valores[4])
            self.input_salario.delete(0, tk.END)
            self.input_salario.insert(0, valores[5])
            self.combo_sucursal.set(valores[6])

    def validar_campos(self):
        if not all([
            self.input_nombre.get().strip(),
            self.input_apellido.get().strip(),
            self.input_cargo.get().strip(),
            self.input_fecha.get().strip(),
            self.input_salario.get().strip(),
            self.combo_sucursal.get().strip()
        ]):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return False
        return True

    def agregar_empleado(self):
        if not self.validar_campos():
            return
        try:
            EmpleadoController.agregar_empleado(
                self.input_nombre.get().strip(),
                self.input_apellido.get().strip(),
                self.input_cargo.get().strip(),
                self.input_fecha.get().strip(),
                self.input_salario.get().strip(),
                self.sucursales[self.combo_sucursal.get()]
            )
            messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el empleado: {e}")

    def actualizar_empleado(self):
        if not self.validar_campos():
            return
        id_empleado = self.input_id.get().strip()
        if not id_empleado or id_empleado == "ID (auto)":
            messagebox.showwarning("Advertencia", "Seleccione un empleado de la tabla.")
            return
        try:
            EmpleadoController.actualizar_empleado(
                id_empleado,
                self.input_nombre.get().strip(),
                self.input_apellido.get().strip(),
                self.input_cargo.get().strip(),
                self.input_fecha.get().strip(),
                self.input_salario.get().strip(),
                self.sucursales[self.combo_sucursal.get()]
            )
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el empleado: {e}")

    def eliminar_empleado(self):
        id_empleado = self.input_id.get().strip()
        if not id_empleado or id_empleado == "ID (auto)":
            messagebox.showwarning("Advertencia", "Seleccione un empleado de la tabla.")
            return
        if messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar al empleado ID {id_empleado}?"):
            try:
                EmpleadoController.eliminar_empleado(id_empleado)
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el empleado: {e}")

    def limpiar_campos(self):
        self.input_id.config(state="normal")
        self.input_id.delete(0, tk.END)
        self.input_id.insert(0, "ID (auto)")
        self.input_id.config(state="disabled")
        self.input_nombre.delete(0, tk.END)
        self.input_apellido.delete(0, tk.END)
        self.input_cargo.delete(0, tk.END)
        self.input_fecha.delete(0, tk.END)
        self.input_salario.delete(0, tk.END)
        self.combo_sucursal.set("")