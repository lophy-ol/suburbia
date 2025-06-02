import tkinter as tk
from tkinter import ttk, messagebox
from controllers.ventas_controller import VentasController

class VentasView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Ventas - TIENDA SUBURBIA")
        self.root.geometry("1000x400")

        self.controller = VentasController()

        # Variables para manejar ids ocultos y textos visibles
        self.clientes = []
        self.empleados = []
        self.metodos_pago = []

        self.crear_widgets()
        self.cargar_listas_relacionadas()
        self.cargar_datos()

    def crear_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        columnas = ("ID Venta", "Tipo Cliente", "ID Cliente", "ID Empleado", "Código Artículo",
                    "Nombre Artículo", "Cantidad", "ID Modo Pago", "Total")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor=tk.W)

        self.tabla.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tabla.yview)
        scrollbar.grid(row=0, column=3, sticky="ns")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        form_frame = tk.LabelFrame(main_frame, text="Datos de la Venta", padx=10, pady=10)
        form_frame.grid(row=1, column=0, columnspan=4, sticky="ew")

        # Labels y widgets
        # ID Venta (Entry editable)
        tk.Label(form_frame, text="ID Venta").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.id_venta_var = tk.StringVar()
        self.id_venta_entry = tk.Entry(form_frame, textvariable=self.id_venta_var, width=25)  # ← se eliminó state="readonly"
        self.id_venta_entry.grid(row=0, column=1, sticky="w", padx=5, pady=3)


        # Tipo Cliente (Combobox)
        tk.Label(form_frame, text="Tipo Cliente").grid(row=0, column=2, sticky="e", padx=5, pady=3)
        self.tipo_cliente_var = tk.StringVar()
        self.tipo_cliente_combo = ttk.Combobox(form_frame, textvariable=self.tipo_cliente_var,
                                               values=["General", "Particular"], state="readonly", width=23)
        self.tipo_cliente_combo.grid(row=0, column=3, sticky="w", padx=5, pady=3)
        self.tipo_cliente_combo.bind("<<ComboboxSelected>>", self.actualizar_tipo_cliente)

        # Cliente (Combobox) - si General id_cliente = 4
        tk.Label(form_frame, text="Cliente").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        self.cliente_var = tk.StringVar()
        self.cliente_combo = ttk.Combobox(form_frame, textvariable=self.cliente_var, state="readonly", width=25)
        self.cliente_combo.grid(row=1, column=1, sticky="w", padx=5, pady=3)

        # Empleado (Combobox)
        tk.Label(form_frame, text="Empleado").grid(row=1, column=2, sticky="e", padx=5, pady=3)
        self.empleado_var = tk.StringVar()
        self.empleado_combo = ttk.Combobox(form_frame, textvariable=self.empleado_var, state="readonly", width=23)
        self.empleado_combo.grid(row=1, column=3, sticky="w", padx=5, pady=3)

        # Código Artículo (Entry)
        tk.Label(form_frame, text="Código Artículo").grid(row=2, column=0, sticky="e", padx=5, pady=3)
        self.codigo_articulo_var = tk.StringVar()
        self.codigo_articulo_entry = tk.Entry(form_frame, textvariable=self.codigo_articulo_var, width=25)
        self.codigo_articulo_entry.grid(row=2, column=1, sticky="w", padx=5, pady=3)
        self.codigo_articulo_entry.bind("<FocusOut>", self.obtener_nombre_precio_articulo)

        # Nombre Artículo (Entry disabled)
        tk.Label(form_frame, text="Nombre Artículo").grid(row=2, column=2, sticky="e", padx=5, pady=3)
        self.nombre_articulo_var = tk.StringVar()
        self.nombre_articulo_entry = tk.Entry(form_frame, textvariable=self.nombre_articulo_var,
                                             state="disabled", width=23)
        self.nombre_articulo_entry.grid(row=2, column=3, sticky="w", padx=5, pady=3)

        # Cantidad (Entry)
        tk.Label(form_frame, text="Cantidad").grid(row=3, column=0, sticky="e", padx=5, pady=3)
        self.cantidad_var = tk.StringVar()
        self.cantidad_entry = tk.Entry(form_frame, textvariable=self.cantidad_var, width=25)
        self.cantidad_entry.grid(row=3, column=1, sticky="w", padx=5, pady=3)
        self.cantidad_entry.bind("<FocusOut>", self.calcular_total)

        # Método de Pago (Combobox)
        tk.Label(form_frame, text="Método de Pago").grid(row=3, column=2, sticky="e", padx=5, pady=3)
        self.modo_pago_var = tk.StringVar()
        self.modo_pago_combo = ttk.Combobox(form_frame, textvariable=self.modo_pago_var,
                                            state="readonly", width=23)
        self.modo_pago_combo.grid(row=3, column=3, sticky="w", padx=5, pady=3)

        # Total (Entry disabled)
        tk.Label(form_frame, text="Total").grid(row=4, column=0, sticky="e", padx=5, pady=3)
        self.total_var = tk.StringVar()
        self.total_entry = tk.Entry(form_frame, textvariable=self.total_var, state="disabled", width=25)
        self.total_entry.grid(row=4, column=1, sticky="w", padx=5, pady=3)

        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=4, pady=10)

        tk.Button(btn_frame, text="Agregar", command=self.agregar_venta).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="Actualizar", command=self.actualizar_venta).grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_venta).grid(row=0, column=2, padx=8)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=3, padx=8)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def cargar_listas_relacionadas(self):
        # Cargar clientes, empleados y métodos de pago desde el controlador
        self.clientes = self.controller.obtener_clientes()       # Lista de dicts con 'id' y 'nombre'
        self.empleados = self.controller.obtener_empleados()     # Igual
        self.metodos_pago = self.controller.obtener_metodos_pago() # Igual

        # Llenar combo clientes
        clientes_nombres = [c["Nombre"] for c in self.clientes]
        self.cliente_combo["values"] = clientes_nombres

        # Llenar combo empleados
        empleados_nombres = [e["nombre_empleado"] for e in self.empleados]
        self.empleado_combo["values"] = empleados_nombres

        # Llenar combo métodos de pago
        modos_pago_nombres = [m["tipo"] for m in self.metodos_pago]
        self.modo_pago_combo["values"] = modos_pago_nombres

        # Por defecto tipo cliente General
        self.tipo_cliente_var.set("General")
        self.actualizar_tipo_cliente()

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        ventas = self.controller.obtener_ventas()
        for venta in ventas:
            self.tabla.insert("", "end", values=(
                venta["id_venta"],
                venta["tipo_cliente"],
                venta["id_cliente"],
                venta["id_empleado"],
                venta["codigo_articulo"],
                venta["nombre_articulo"],
                venta["cantidad"],
                venta["id_modo_pago"],
                venta["total"]
            ))

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.focus()
        if seleccionado:
            valores = self.tabla.item(seleccionado, "values")

            # Asignar valores a widgets
            self.id_venta_var.set(valores[0])
            self.tipo_cliente_var.set(valores[1])

            # Seleccionar cliente por id y mostrar nombre
            id_cliente = valores[2]
            cliente_nombre = self._buscar_nombre_por_id(self.clientes, id_cliente, "cliente","Nombre")
            self.cliente_var.set(cliente_nombre)

            # Seleccionar empleado
            id_empleado = valores[3]
            empleado_nombre = self._buscar_nombre_por_id(self.empleados, id_empleado, "empleado" ,"Nombre")
            self.empleado_var.set(empleado_nombre)

            self.codigo_articulo_var.set(valores[4])
            self.nombre_articulo_var.set(valores[5])
            self.cantidad_var.set(valores[6])

            # Método pago
            id_modo_pago = valores[7]
            modo_pago_nombre = self._buscar_nombre_por_id(self.metodos_pago, id_modo_pago, "modo_pago" ,"tipo")
            self.modo_pago_var.set(modo_pago_nombre)

            self.total_var.set(valores[8])

            # Bloquear/activar cliente segun tipo cliente
            self.actualizar_tipo_cliente()

    def _buscar_nombre_por_id(self, lista, id_buscar, modulo, nombre):
        for item in lista:
            if str(item[f"id_{modulo}"]) == str(id_buscar):
                return item[nombre]
        return ""

    def _buscar_id_por_nombre(self, lista, nombre_buscar, modulo, nombre):
        for item in lista:
            if item[nombre] == nombre_buscar:
                return item[f"id_{modulo}"]
        return None

    def actualizar_tipo_cliente(self, event=None):
        tipo = self.tipo_cliente_var.get()
        if tipo == "General":
            # ID Cliente = 4 fijo, deshabilitar combo
            cliente_general = next((c for c in self.clientes if c["id_cliente"] == 4), None)
            if cliente_general:
                self.cliente_var.set(cliente_general["Nombre"])
            else:
                self.cliente_var.set("")
            self.cliente_combo.config(state="disabled")
        else:
            self.cliente_combo.config(state="readonly")
            self.cliente_var.set("")

    def obtener_nombre_precio_articulo(self, event=None):
        codigo = self.codigo_articulo_var.get().strip()
        if not codigo:
            self.nombre_articulo_var.set("")
            self.total_var.set("")
            return

        # Consultar al controlador
        articulo = self.controller.obtener_articulo_por_codigo(codigo)
        if articulo:
            self.nombre_articulo_var.set(articulo["nombre_articulo"])
            self.calcular_total()
        else:
            self.nombre_articulo_var.set("")
            self.total_var.set("")
            messagebox.showwarning("Aviso", "Código de artículo no encontrado.")

    def calcular_total(self, event=None):
        try:
            cantidad = int(self.cantidad_var.get())
            precio_unitario = 0
            codigo = self.codigo_articulo_var.get().strip()
            if codigo:
                articulo = self.controller.obtener_articulo_por_codigo(codigo)
                if articulo:
                    precio_unitario = float(articulo["precio"])
            total = cantidad * precio_unitario * 1.16
            self.total_var.set(f"{total:.2f}")
        except Exception:
            self.total_var.set("")

    def validar_campos(self):
        if not self.tipo_cliente_var.get():
            messagebox.showwarning("Advertencia", "Seleccione el tipo de cliente.")
            return False

        if self.tipo_cliente_var.get() == "Particular" and not self.cliente_var.get():
            messagebox.showwarning("Advertencia", "Seleccione un cliente.")
            return False

        if not self.empleado_var.get():
            messagebox.showwarning("Advertencia", "Seleccione un empleado.")
            return False

        if not self.codigo_articulo_var.get():
            messagebox.showwarning("Advertencia", "Ingrese código de artículo.")
            return False

        try:
            cantidad = int(self.cantidad_var.get())
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "Cantidad debe ser mayor que cero.")
                return False
        except ValueError:
            messagebox.showwarning("Advertencia", "Cantidad debe ser un número entero.")
            return False

        if not self.modo_pago_var.get():
            messagebox.showwarning("Advertencia", "Seleccione método de pago.")
            return False

        return True

    def agregar_venta(self):
        if not self.validar_campos():
            return

        tipo_cliente = self.tipo_cliente_var.get()
        if tipo_cliente == "General":
            id_cliente = 4  # fijo
        else:
            id_cliente = self._buscar_id_por_nombre(self.clientes, self.cliente_var.get(), "cliente", "Nombre")
            if id_cliente is None:
                messagebox.showerror("Error", "Cliente no válido.")
                return

        id_empleado = self._buscar_id_por_nombre(self.empleados, self.empleado_var.get(), "empleado", "nombre_empleado")
        if id_empleado is None:
            messagebox.showerror("Error", "Empleado no válido.")
            return

        id_modo_pago = self._buscar_id_por_nombre(self.metodos_pago, self.modo_pago_var.get(), "modo_pago", "tipo")
        if id_modo_pago is None:
            messagebox.showerror("Error", "Método de pago no válido.")
            return

        id_venta = self.id_venta_var.get().strip()
        if not id_venta:
            messagebox.showerror("Error", "El campo ID Venta no puede estar vacío.")
            return

        codigo_articulo = self.codigo_articulo_var.get().strip()
        nombre_articulo = self.nombre_articulo_var.get().strip()
        cantidad = int(self.cantidad_var.get())
        total = float(self.total_var.get())

        if self.controller.agregar_venta(
            id_venta,
            total,
            id_cliente,
            id_empleado,
            tipo_cliente,
            codigo_articulo,
            cantidad,
            id_modo_pago,
            nombre_articulo
        ):
            messagebox.showinfo("Éxito", "Venta agregada correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo agregar la venta.")


    def actualizar_venta(self):
        if not self.validar_campos():
            return

        if not self.id_venta_var.get():
            messagebox.showwarning("Advertencia", "Seleccione una venta para actualizar.")
            return

        tipo_cliente = self.tipo_cliente_var.get()
        if tipo_cliente == "General":
            id_cliente = 4  # fijo
        else:
            id_cliente = self._buscar_id_por_nombre(self.clientes, self.cliente_var.get(), "cliente", "Nombre")
            if id_cliente is None:
                messagebox.showerror("Error", "Cliente no válido.")
                return

        id_empleado = self._buscar_id_por_nombre(self.empleados, self.empleado_var.get(), "empleado", "Nombre")
        if id_empleado is None:
            messagebox.showerror("Error", "Empleado no válido.")
            return

        id_modo_pago = self._buscar_id_por_nombre(self.metodos_pago, self.modo_pago_var.get(), "modo_pago", "tipo")
        if id_modo_pago is None:
            messagebox.showerror("Error", "Método de pago no válido.")
            return

        codigo_articulo = self.codigo_articulo_var.get().strip()
        nombre_articulo = self.nombre_articulo_var.get().strip()
        cantidad = int(self.cantidad_var.get())
        total = float(self.total_var.get())
        id_venta = int(self.id_venta_var.get())

        if self.controller.actualizar_venta(
            id_venta,
            total,
            id_cliente,
            id_empleado,
            tipo_cliente,
            codigo_articulo,
            cantidad,
            id_modo_pago,
            nombre_articulo
        ):
            messagebox.showinfo("Éxito", "Venta actualizada correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la venta.")

    def eliminar_venta(self):
        id_venta = self.id_venta_var.get()
        if not id_venta:
            messagebox.showwarning("Advertencia", "Seleccione una venta para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta venta?"):
            if self.controller.eliminar_venta(int(id_venta)):
                messagebox.showinfo("Éxito", "Venta eliminada correctamente.")
                self.cargar_datos()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la venta.")

    def limpiar_campos(self):
        self.id_venta_var.set("")
        self.tipo_cliente_var.set("General")
        self.cliente_var.set("")
        self.empleado_var.set("")
        self.codigo_articulo_var.set("")
        self.nombre_articulo_var.set("")
        self.cantidad_var.set("")
        self.modo_pago_var.set("")
        self.total_var.set("")
        self.actualizar_tipo_cliente()


if __name__ == "__main__":
    root = tk.Tk()
    app = VentasView(root)
    root.mainloop()
