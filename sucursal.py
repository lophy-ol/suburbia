import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.exc import SQLAlchemyError
from conexion import SessionLocal
from models import Sucursal  # Asegúrate de tener este modelo definido

class SucursalFrame(ttk.Frame):
    def __init__(self, parent, return_callback):
        super().__init__(parent)
        self.return_callback = return_callback
        self.create_widgets()
        self.load_sucursales()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=5)

        ttk.Button(top_frame, text="Volver", command=self.return_callback).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Agregar Sucursal", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)

        columns = ['ID', 'Nombre', 'Dirección', 'Ciudad', 'Estado', 'Código Postal', 'Teléfono']
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<Double-1>', self.edit_sucursal)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Editar", command=lambda: self.edit_sucursal(None)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_sucursal).pack(side=tk.LEFT, padx=5)

    def load_sucursales(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            db = SessionLocal()
            sucursales = db.query(Sucursal).order_by(Sucursal.id_sucursal).all()

            for s in sucursales:
                self.tree.insert('', tk.END, values=(s.id_sucursal, s.nombre, s.direccion, s.ciudad, s.estado, s.codigo_postal, s.telefono))
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudieron cargar las sucursales: {str(e)}")
        finally:
            db.close()

    def open_add_dialog(self, sucursal=None):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Editar Sucursal" if sucursal else "Agregar Sucursal")
        self.dialog.grab_set()

        self.sucursal_editando = sucursal

        labels = ["ID", "Nombre", "Direccion", "Ciudad", "Estado", "Codigo Postal", "Telefono"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.dialog, text=label + ":").grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
            entry = ttk.Entry(self.dialog, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label.lower().replace(" ", "_")] = entry

        if sucursal:
            self.entries["id"].insert(0, sucursal[0])
            self.entries["id"].config(state='readonly')
            for i, key in enumerate(["nombre", "direccion", "ciudad", "estado", "codigo_postal", "telefono"]):
                self.entries[key].insert(0, sucursal[i+1])

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self.save_sucursal).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)

    def save_sucursal(self):
        try:
            data = {key: entry.get().strip() for key, entry in self.entries.items()}
            if not all(data[k] for k in data if k != 'id'):
                messagebox.showwarning("Validación", "Todos los campos son obligatorios")
                return

            db = SessionLocal()
            if self.sucursal_editando:
                suc = db.query(Sucursal).filter_by(id_sucursal=data["id"]).first()
                if suc:
                    for k, v in data.items():
                        if k != 'id':
                            setattr(suc, k, v)
                    db.commit()
                    messagebox.showinfo("Éxito", "Sucursal actualizada")
            else:
                nueva = Sucursal(**{k: v for k, v in data.items() if k != 'id'})
                db.add(nueva)
                db.commit()
                messagebox.showinfo("Éxito", "Sucursal agregada")

            self.load_sucursales()
            self.dialog.destroy()
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
        finally:
            db.close()

    def edit_sucursal(self, event):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una sucursal")
            return

        item = self.tree.item(selected[0])
        self.open_add_dialog(item['values'])

    def delete_sucursal(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una sucursal")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta sucursal?"):
            return

        sucursal_id = self.tree.item(selected[0])['values'][0]

        try:
            db = SessionLocal()
            suc = db.query(Sucursal).filter_by(id_sucursal=sucursal_id).first()
            if suc:
                db.delete(suc)
                db.commit()
                messagebox.showinfo("Éxito", "Sucursal eliminada")
                self.load_sucursales()
            else:
                messagebox.showerror("Error", "Sucursal no encontrada")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
        finally:
            db.close()
