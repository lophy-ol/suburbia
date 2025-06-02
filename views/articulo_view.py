import tkinter as tk
from tkinter import ttk, messagebox
from controllers.articulo_controller import ArticuloController

class ArticuloView:
    def __init__(self, root):
        self.root = root
        self.controller = ArticuloController()
        self.codigo_seleccionado = None
        self.categorias_dict = {}
        self.marcas_dict = {}

        self.root.title("Gestión de Artículos - TIENDA SUBURBIA")
        self.root.geometry("1000x400")
        
        self.crear_widgets()
        self.cargar_datos_iniciales()
        self.cargar_datos()

    def crear_widgets(self):
        # Frame principal con fondo claro
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Tabla de artículos con estilo mejorado
        columnas = ("Código", "Nombre", "Estado", "Precio", "Gasto", "Stock", "Categoría", "Marca")
        self.tabla = ttk.Treeview(
            main_frame, 
            columns=columnas, 
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col, anchor=tk.CENTER)
            self.tabla.column(col, width=120, anchor=tk.CENTER)
        
        self.tabla.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tabla.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        # Formulario con LabelFrame
        form_frame = tk.LabelFrame(
            main_frame, 
            text="Datos del Artículo", 
            padx=10, 
            pady=10,
            bg="#f0f0f0",
            font=('Helvetica', 10, 'bold')
        )
        form_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Campos del formulario organizados en 2 columnas
        self.inputs = {}
        campos = [
            ("Código:", "codigo", False),
            ("Nombre:", "nombre", False),
            ("Precio:", "precio", False),
            ("Gasto:", "gasto", False),
            ("Stock:", "stock", False),
            ("Categoría:", "categoria", False),
            ("Marca:", "marca", False),
            ("Estado:", "estado", False)
        ]

        for i, (label, key, readonly) in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(
                form_frame, 
                text=label, 
                bg="#f0f0f0",
                anchor="e"
            ).grid(row=row, column=col, sticky="e", padx=5, pady=2)
            
            if key in ["categoria", "marca"]:
                combo = ttk.Combobox(form_frame, state="readonly")
                combo.grid(row=row, column=col+1, sticky="ew", padx=5, pady=2)
                self.inputs[key] = combo
            elif key == "estado":
                self.estado_var = tk.IntVar()
                check = tk.Checkbutton(
                    form_frame, 
                    text="Activado", 
                    variable=self.estado_var,
                    bg="#f0f0f0"
                )
                check.grid(row=row, column=col+1, sticky="w", padx=5, pady=2)
                self.inputs[key] = self.estado_var
            else:
                entry = tk.Entry(form_frame, width=25)
                if readonly:
                    entry.config(state="disabled")
                entry.grid(row=row, column=col+1, sticky="ew", padx=5, pady=2)
                self.inputs[key] = entry

        # Configurar expansión de columnas
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # Botones con estilo consistente
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        btn_agregar = tk.Button(
            btn_frame, 
            text="Agregar", 
            command=self.agregar_articulo,
            width=12,
            bg="#4CAF50",
            fg="white"
        )
        btn_actualizar = tk.Button(
            btn_frame, 
            text="Actualizar", 
            command=self.actualizar_articulo,
            width=12,
            bg="#2196F3",
            fg="white"
        )
        btn_eliminar = tk.Button(
            btn_frame, 
            text="Eliminar", 
            command=self.eliminar_articulo,
            width=12,
            bg="#f44336",
            fg="white"
        )
        btn_limpiar = tk.Button(
            btn_frame, 
            text="Limpiar", 
            command=self.limpiar_campos,
            width=12,
            bg="#607D8B",
            fg="white"
        )

        btn_agregar.grid(row=0, column=0, padx=5)
        btn_actualizar.grid(row=0, column=1, padx=5)
        btn_eliminar.grid(row=0, column=2, padx=5)
        btn_limpiar.grid(row=0, column=3, padx=5)

        # Configurar el redimensionamiento
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def cargar_datos_iniciales(self):
        # Cargar categorías
        categorias = self.controller.obtener_categorias()
        nombres_categorias = []
        self.categorias_dict.clear()
        for cat in categorias:
            self.categorias_dict[cat['tipo_categoria']] = cat['id_categorias']
            nombres_categorias.append(cat['tipo_categoria'])
        self.inputs["categoria"]["values"] = nombres_categorias

        # Cargar marcas
        marcas = self.controller.obtener_marcas()
        nombres_marcas = []
        self.marcas_dict.clear()
        for marca in marcas:
            self.marcas_dict[marca['nombre_marca']] = marca['id_marca']
            nombres_marcas.append(marca['nombre_marca'])
        self.inputs["marca"]["values"] = nombres_marcas

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        articulos = self.controller.obtener_articulos()
        for art in articulos:
            self.tabla.insert("", "end", values=(
                art["codigo_articulo"],
                art["nombre_articulo"],
                "Activado" if art["activacion_articulo"] else "Desactivado",
                f"${art['precio']:.2f}",
                f"${art.get('gasto', 0):.2f}",
                art["stock"],
                art.get("tipo_categoria", ""),
                art.get("nombre_marca", "")
            ))

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.focus()
        if seleccionado:
            valores = self.tabla.item(seleccionado, "values")
            self.codigo_seleccionado = valores[0]
            
            self.inputs["codigo"].config(state="normal")
            self.inputs["codigo"].delete(0, tk.END)
            self.inputs["codigo"].insert(0, valores[0])
            self.inputs["codigo"].config(state="disabled")
            
            self.inputs["nombre"].delete(0, tk.END)
            self.inputs["nombre"].insert(0, valores[1])
            
            self.inputs["estado"].set(1 if valores[2] == "Activado" else 0)
            
            precio = valores[3].replace("$", "").strip()
            self.inputs["precio"].delete(0, tk.END)
            self.inputs["precio"].insert(0, precio)
            
            gasto = valores[4].replace("$", "").strip()
            self.inputs["gasto"].delete(0, tk.END)
            self.inputs["gasto"].insert(0, gasto)
            
            self.inputs["stock"].delete(0, tk.END)
            self.inputs["stock"].insert(0, valores[5])
            
            self.inputs["categoria"].set(valores[6])
            self.inputs["marca"].set(valores[7])

    def validar_campos(self):
        campos_requeridos = ["nombre", "precio", "stock", "categoria", "marca"]
        for campo in campos_requeridos:
            if not self.inputs[campo].get().strip() if hasattr(self.inputs[campo], 'get') else not self.inputs[campo].get():
                messagebox.showwarning("Advertencia", f"El campo {campo.capitalize()} es requerido.")
                return False
        
        try:
            float(self.inputs["precio"].get())
            float(self.inputs["gasto"].get())
            int(self.inputs["stock"].get())
        except ValueError:
            messagebox.showwarning("Advertencia", "Precio, Gasto y Stock deben ser valores numéricos válidos.")
            return False
            
        return True

    def agregar_articulo(self):
        if not self.validar_campos():
            return
        
        try:
            codigo = self.inputs["codigo"].get().strip()
            nombre = self.inputs["nombre"].get().strip()
            activado = self.inputs["estado"].get()
            precio = float(self.inputs["precio"].get())
            gasto = float(self.inputs["gasto"].get())
            stock = int(self.inputs["stock"].get())
            categoria = self.categorias_dict[self.inputs["categoria"].get()]
            marca = self.marcas_dict[self.inputs["marca"].get()]

            exito, mensaje = self.controller.agregar_articulo(
                codigo, nombre, activado, precio, stock, gasto, categoria, marca
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_datos()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def actualizar_articulo(self):
        if not self.codigo_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un artículo de la tabla.")
            return
            
        if not self.validar_campos():
            return
        
        try:
            nombre = self.inputs["nombre"].get().strip()
            activado = self.inputs["estado"].get()
            precio = float(self.inputs["precio"].get())
            gasto = float(self.inputs["gasto"].get())
            stock = int(self.inputs["stock"].get())
            categoria = self.categorias_dict[self.inputs["categoria"].get()]
            marca = self.marcas_dict[self.inputs["marca"].get()]

            exito, mensaje = self.controller.actualizar_articulo(
                self.codigo_seleccionado, nombre, activado, precio, stock, gasto, categoria, marca
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_datos()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def eliminar_articulo(self):
        if not self.codigo_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un artículo de la tabla.")
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el artículo con código {self.codigo_seleccionado}?"
        )
        
        if confirmacion:
            try:
                exito, mensaje = self.controller.eliminar_articulo(self.codigo_seleccionado)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.cargar_datos()
                    self.limpiar_campos()
                else:
                    messagebox.showerror("Error", mensaje)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def limpiar_campos(self):
        self.codigo_seleccionado = None
        for key, widget in self.inputs.items():
            if key == "codigo":
                widget.config(state="normal")
                widget.delete(0, tk.END)
                widget.insert(0, "Nuevo")
                widget.config(state="disabled")
            elif key == "estado":
                widget.set(1)
            elif hasattr(widget, 'set'):
                widget.set("")
            elif hasattr(widget, 'delete'):
                widget.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = ArticuloView(root)
    root.mainloop()

if __name__ == "__main__":
    main()