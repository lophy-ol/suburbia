import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.exc import SQLAlchemyError
from conexion import SessionLocal
from models import Almacen  # Asegúrate de tener este modelo definido

class AlmacenFrame(ttk.Frame):
    def __init__(self, parent, return_callback):
        super().__init__(parent)
        self.return_callback = return_callback
        self.create_widgets()
        self.load_almacenes()
    
    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(top_frame, text="Volver", command=self.return_callback).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Agregar Almacén", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)
        
        columns = ['ID', 'Nombre', 'Ubicación', 'Capacidad', 'Estado']
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', self.edit_almacen)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Editar", command=lambda: self.edit_almacen(None)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_almacen).pack(side=tk.LEFT, padx=5)
    
    def load_almacenes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            db = SessionLocal()
            almacenes = db.query(Almacen).order_by(Almacen.nombre).all()
            
            for a in almacenes:
                self.tree.insert('', tk.END, values=(
                    a.idalmacen,
                    a.nombre,
                    a.ubicacion,
                    a.capacidad_maxima,
                    a.estado
                ))
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo cargar almacenes: {str(e)}")
        finally:
            db.close()
    
    def open_add_dialog(self, almacen=None):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Editar Almacén" if almacen else "Agregar Almacén")
        self.dialog.grab_set()
        
        self.almacen_editando = almacen
        
        fields = [
            ('idalmacen', 'ID:', 0),
            ('nombre', 'Nombre:', 1),
            ('ubicacion', 'Ubicación:', 2),
            ('capacidad_maxima', 'Capacidad Máxima:', 3),
            ('estado', 'Estado:', 4)
        ]
        
        self.entries = {}
        for field, label, row in fields:
            ttk.Label(self.dialog, text=label).grid(row=row, column=0, padx=5, pady=5, sticky=tk.E)
            entry = ttk.Entry(self.dialog, width=30)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries[field] = entry
        
        if almacen:
            self.entries['idalmacen'].insert(0, almacen[0])
            self.entries['idalmacen'].config(state='readonly')
            self.entries['nombre'].insert(0, almacen[1])
            self.entries['ubicacion'].insert(0, almacen[2])
            self.entries['capacidad_maxima'].insert(0, almacen[3])
            self.entries['estado'].insert(0, almacen[4])
        
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Guardar", command=self.save_almacen).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def save_almacen(self):
        try:
            data = {
                'idalmacen': self.entries['idalmacen'].get(),
                'nombre': self.entries['nombre'].get(),
                'ubicacion': self.entries['ubicacion'].get(),
                'capacidad_maxima': self.entries['capacidad_maxima'].get(),
                'estado': self.entries['estado'].get()
            }
            
            if not data['nombre']:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            db = SessionLocal()
            
            if self.almacen_editando:
                a = db.query(Almacen).filter_by(idalmacen=data['idalmacen']).first()
                if a:
                    a.nombre = data['nombre']
                    a.ubicacion = data['ubicacion']
                    a.capacidad_maxima = int(data['capacidad_maxima'])
                    a.estado = data['estado']
                    db.commit()
                    messagebox.showinfo("Éxito", "Almacén actualizado")
            else:
                nuevo = Almacen(
                    nombre=data['nombre'],
                    ubicacion=data['ubicacion'],
                    capacidad_maxima=int(data['capacidad_maxima']),
                    estado=data['estado']
                )
                db.add(nuevo)
                db.commit()
                messagebox.showinfo("Éxito", "Almacén agregado")
            
            self.load_almacenes()
            self.dialog.destroy()
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo guardar el almacén: {str(e)}")
        finally:
            db.close()
    
    def edit_almacen(self, event):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un almacén")
            return
        
        item = self.tree.item(selected[0])
        self.open_add_dialog(item['values'])
    
    def delete_almacen(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un almacén")
            return
        
        if not messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este almacén?"):
            return
        
        almacen_id = self.tree.item(selected[0])['values'][0]
        
        try:
            db = SessionLocal()
            almacen = db.query(Almacen).filter_by(idalmacen=almacen_id).first()
            if almacen:
                db.delete(almacen)
                db.commit()
                messagebox.showinfo("Éxito", "Almacén eliminado correctamente")
                self.load_almacenes()
            else:
                messagebox.showerror("Error", "No se encontró el almacén")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
        finally:
            db.close()
