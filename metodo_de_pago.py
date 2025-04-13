import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.exc import SQLAlchemyError
from conexion import SessionLocal
from models import MetodoPago  # Asegúrate de tener este modelo definido

class MetodoPagoFrame(ttk.Frame):
    def __init__(self, parent, return_callback):
        super().__init__(parent)
        self.return_callback = return_callback
        self.create_widgets()
        self.load_metodos_pago()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=5)

        ttk.Button(top_frame, text="Volver", command=self.return_callback).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Agregar Método", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)

        columns = ['ID', 'Nombre', 'Descripción', 'Activo']
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<Double-1>', self.edit_metodo)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Editar", command=lambda: self.edit_metodo(None)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_metodo).pack(side=tk.LEFT, padx=5)

    def load_metodos_pago(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            db = SessionLocal()
            metodos = db.query(MetodoPago).order_by(MetodoPago.idmetodo_pago).all()

            for m in metodos:
                self.tree.insert('', tk.END, values=(m.idmetodo_pago, m.nombre, m.descripcion, m.activo))
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudieron cargar los métodos: {str(e)}")
        finally:
            db.close()

    def open_add_dialog(self, metodo=None):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Editar Método de Pago" if metodo else "Agregar Método de Pago")
        self.dialog.grab_set()

        self.metodo_editando = metodo

        ttk.Label(self.dialog, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.id_entry = ttk.Entry(self.dialog, width=30)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.dialog, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.nombre_entry = ttk.Entry(self.dialog, width=30)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.dialog, text="Descripción:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.descripcion_entry = ttk.Entry(self.dialog, width=30)
        self.descripcion_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.dialog, text="Activo:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.activo_var = tk.StringVar(value='Sí')
        activo_cb = ttk.Combobox(self.dialog, textvariable=self.activo_var, values=['Sí', 'No'], state='readonly', width=28)
        activo_cb.grid(row=3, column=1, padx=5, pady=5)

        if metodo:
            self.id_entry.insert(0, metodo[0])
            self.id_entry.config(state='readonly')
            self.nombre_entry.insert(0, metodo[1])
            self.descripcion_entry.insert(0, metodo[2])
            self.activo_var.set(metodo[3])

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self.save_metodo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)

    def save_metodo(self):
        try:
            idmetodo = self.id_entry.get()
            nombre = self.nombre_entry.get().strip()
            descripcion = self.descripcion_entry.get().strip()
            activo = self.activo_var.get()

            if not nombre:
                messagebox.showwarning("Validación", "El nombre es obligatorio")
                return

            db = SessionLocal()
            if self.metodo_editando:
                metodo = db.query(MetodoPago).filter_by(idmetodo_pago=idmetodo).first()
                if metodo:
                    metodo.nombre = nombre
                    metodo.descripcion = descripcion
                    metodo.activo = activo
                    db.commit()
                    messagebox.showinfo("Éxito", "Método actualizado")
            else:
                nuevo = MetodoPago(nombre=nombre, descripcion=descripcion, activo=activo)
                db.add(nuevo)
                db.commit()
                messagebox.showinfo("Éxito", "Método agregado")

            self.load_metodos_pago()
            self.dialog.destroy()
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
        finally:
            db.close()

    def edit_metodo(self, event):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un método de pago")
            return

        item = self.tree.item(selected[0])
        self.open_add_dialog(item['values'])

    def delete_metodo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un método de pago")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este método?"):
            return

        metodo_id = self.tree.item(selected[0])['values'][0]

        try:
            db = SessionLocal()
            metodo = db.query(MetodoPago).filter_by(idmetodo_pago=metodo_id).first()
            if metodo:
                db.delete(metodo)
                db.commit()
                messagebox.showinfo("Éxito", "Método eliminado")
                self.load_metodos_pago()
            else:
                messagebox.showerror("Error", "Método no encontrado")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
        finally:
            db.close()
