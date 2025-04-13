import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.exc import SQLAlchemyError
from conexion import SessionLocal
from models import Proveedor  # Asegúrate de que el modelo esté creado

class ProveedorFrame(ttk.Frame):
    def __init__(self, parent, return_callback):
        super().__init__(parent)
        self.return_callback = return_callback
        self.create_widgets()
        self.load_proveedores()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=5)

        ttk.Button(top_frame, text="Volver", command=self.return_callback).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Agregar Proveedor", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)

        columns = ['ID', 'Nombre', 'Teléfono', 'Correo', 'Dirección']
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<Double-1>', self.edit_proveedor)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Editar", command=lambda: self.edit_proveedor(None)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_proveedor).pack(side=tk.LEFT, padx=5)

    def load_proveedores(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            db = SessionLocal()
            proveedores = db.query(Proveedor).order_by(Proveedor.id_proveedor).all()

            for p in proveedores:
                self.tree.insert('', tk.END, values=(p.id_proveedor, p.nombre, p.telefono, p.correo, p.direccion))
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores: {str(e)}")
        finally:
            db.close()

    def open_add_dialog(self, proveedor=None):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Editar Proveedor" if proveedor else "Agregar Proveedor")
        self.dialog.grab_set()

        self.proveedor_editando = proveedor

        labels = ["ID", "Nombre", "Telefono", "Correo", "Direccion"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.dialog, text=label + ":").grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
            entry = ttk.Entry(self.dialog, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label.lower()] = entry

        if proveedor:
            self.entries["id"].insert(0, proveedor[0])
            self.entries["id"].config(state='readonly')
            for i, key in enumerate(["nombre", "telefono", "correo", "direccion"]):
                self.entries[key].insert(0, proveedor[i+1])

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self.save_proveedor).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)

    def save_proveedor(self):
        try:
            data = {key: entry.get().strip() for key, entry in self.entries.items()}
            if not all(data[k] for k in data if k != 'id'):
                messagebox.showwarning("Validación", "Todos los campos son obligatorios")
                return

            db = SessionLocal()
            if self.proveedor_editando:
                proveedor = db.query(Proveedor).filter_by(id_proveedor=data["id"]).first()
                if proveedor:
                    proveedor.nombre = data["nombre"]
                    proveedor.telefono = data["telefono"]
                    proveedor.correo = data["correo"]
                    proveedor.direccion = data["direccion"]
                    db.commit()
                    messagebox.showinfo("Éxito", "Proveedor actualizado")
            else:
                nuevo = Proveedor(nombre=data["nombre"], telefono=data["telefono"],
                                  correo=data["correo"], direccion=data["direccion"])
                db.add(nuevo)
                db.commit()
                messagebox.showinfo("Éxito", "Proveedor agregado")

            self.load_proveedores()
            self.dialog.destroy()
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
        finally:
            db.close()

    def edit_proveedor(self, event):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor")
            return

        item = self.tree.item(selected[0])
        self.open_add_dialog(item['values'])

    def delete_proveedor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este proveedor?"):
            return

        proveedor_id = self.tree.item(selected[0])['values'][0]

        try:
            db = SessionLocal()
            proveedor = db.query(Proveedor).filter_by(id_proveedor=proveedor_id).first()
            if proveedor:
                db.delete(proveedor)
                db.commit()
                messagebox.showinfo("Éxito", "Proveedor eliminado")
                self.load_proveedores()
            else:
                messagebox.showerror("Error", "Proveedor no encontrado")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
        finally:
            db.close()
