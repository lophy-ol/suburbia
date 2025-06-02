import tkinter as tk
from tkinter import ttk, messagebox
from controllers.cliente_controller import ClienteController

# shfsh

class ClienteView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Clientes - TIENDA SUBURBIA")
        self.root.geometry("800x500")
        
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Tabla de clientes
        columnas = ("ID", "Nombre", "Apellido", "Teléfono", "Correo", "Dirección")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor=tk.W)
        
        self.tabla.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tabla.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        # Formulario
        form_frame = tk.LabelFrame(main_frame, text="Datos del Cliente", padx=5, pady=5)
        form_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.inputs = {}
        labels = ["ID (auto)", "Nombre", "Apellido", "Teléfono", "Correo", "Dirección"]
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i//3, column=i%3*2, sticky="e", padx=5, pady=2)
            entry = tk.Entry(form_frame, width=25)
            entry.grid(row=i//3, column=i%3*2+1, sticky="w", padx=5, pady=2)
            self.inputs[label] = entry
        
        self.inputs["ID (auto)"].config(state="disabled")

        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        btn_agregar = tk.Button(btn_frame, text="Agregar", command=self.agregar_cliente)
        btn_actualizar = tk.Button(btn_frame, text="Actualizar", command=self.actualizar_cliente)
        btn_eliminar = tk.Button(btn_frame, text="Eliminar", command=self.eliminar_cliente)
        btn_limpiar = tk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos)

        btn_agregar.grid(row=0, column=0, padx=5)
        btn_actualizar.grid(row=0, column=1, padx=5)
        btn_eliminar.grid(row=0, column=2, padx=5)
        btn_limpiar.grid(row=0, column=3, padx=5)

        # Configurar el redimensionamiento
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        clientes = ClienteController.obtener_clientes()
        for cliente in clientes:
            self.tabla.insert("", "end", values=(
                cliente["id_cliente"],
                cliente["Nombre"],
                cliente["Apellido"],
                cliente["Telefono"],
                cliente["Correo"],
                cliente["Direccion"]
            ))

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.focus()
        if seleccionado:
            valores = self.tabla.item(seleccionado, "values")
            claves = ["ID (auto)", "Nombre", "Apellido", "Teléfono", "Correo", "Dirección"]
            for i, clave in enumerate(claves):
                entry = self.inputs[clave]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, valores[i])
                if clave == "ID (auto)":
                    entry.config(state="disabled")

    def validar_campos(self):
        campos_requeridos = ["Nombre", "Apellido", "Teléfono"]
        for campo in campos_requeridos:
            if not self.inputs[campo].get().strip():
                messagebox.showwarning("Advertencia", f"El campo {campo} es requerido.")
                return False
        return True

    def agregar_cliente(self):
        if not self.validar_campos():
            return
        
        nombre = self.inputs["Nombre"].get().strip()
        apellido = self.inputs["Apellido"].get().strip()
        telefono = self.inputs["Teléfono"].get().strip()
        correo = self.inputs["Correo"].get().strip()
        direccion = self.inputs["Dirección"].get().strip()

        if ClienteController.agregar_cliente(nombre, apellido, telefono, correo, direccion):
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo agregar el cliente.")

    def actualizar_cliente(self):
        if not self.validar_campos():
            return
        
        id_cliente = self.inputs["ID (auto)"].get().strip()
        if not id_cliente or id_cliente == "ID (auto)":
            messagebox.showwarning("Advertencia", "Seleccione un cliente de la tabla.")
            return
        
        nombre = self.inputs["Nombre"].get().strip()
        apellido = self.inputs["Apellido"].get().strip()
        telefono = self.inputs["Teléfono"].get().strip()
        correo = self.inputs["Correo"].get().strip()
        direccion = self.inputs["Dirección"].get().strip()

        if ClienteController.actualizar_cliente(id_cliente, nombre, apellido, telefono, correo, direccion):
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el cliente.")

    def eliminar_cliente(self):
        id_cliente = self.inputs["ID (auto)"].get().strip()
        if not id_cliente or id_cliente == "ID (auto)":
            messagebox.showwarning("Advertencia", "Seleccione un cliente de la tabla.")
            return
        
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el cliente con ID {id_cliente}?"
        )
        
        if confirmacion:
            if ClienteController.eliminar_cliente(id_cliente):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.cargar_datos()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente.")

    def limpiar_campos(self):
        for clave, entry in self.inputs.items():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            if clave == "ID (auto)":
                entry.insert(0, "ID (auto)")
            entry.config(state="disabled" if clave == "ID (auto)" else "normal")