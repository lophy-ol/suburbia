import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.exc import SQLAlchemyError
from conexion import SessionLocal
from models import Cliente

class ClienteFrame(ttk.Frame):
    def __init__(self, parent, return_callback):
        super().__init__(parent)
        self.return_callback = return_callback
        self.create_widgets()
        self.load_clientes()
    
    def create_widgets(self):
        # Frame superior (botones)
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=5)
        
        # Botones
        btn_volver = ttk.Button(top_frame, text="Volver", command=self.return_callback)
        btn_volver.pack(side=tk.LEFT, padx=5)
        
        btn_agregar = ttk.Button(top_frame, text="Agregar Cliente", command=self.open_add_dialog)
        btn_agregar.pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar clientes
        columns = ['ID', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Dirección']
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col == 'ID' else 150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind doble click para editar
        self.tree.bind('<Double-1>', self.edit_cliente)
        
        # Botones de acción
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)
        
        btn_editar = ttk.Button(btn_frame, text="Editar", command=lambda: self.edit_cliente(None))
        btn_editar.pack(side=tk.LEFT, padx=5)
        
        btn_eliminar = ttk.Button(btn_frame, text="Eliminar", command=self.delete_cliente)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
    
    def load_clientes(self):
        """Carga los clientes desde la base de datos"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            db = SessionLocal()
            clientes = db.query(Cliente).order_by(Cliente.Nombre).all()
            
            for cliente in clientes:
                self.tree.insert('', tk.END, values=(
                    cliente.ID_Cliente,
                    cliente.Nombre,
                    cliente.Apellido or "",
                    cliente.Telefono or "",
                    cliente.Correo or "",
                    cliente.Direccion or ""
                ))
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudieron cargar los clientes: {str(e)}")
        finally:
            db.close()
    
    def open_add_dialog(self, cliente=None):
        """Abre el diálogo para agregar/editar cliente"""
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Editar Cliente" if cliente else "Agregar Cliente")
        self.dialog.grab_set()
        
        self.cliente_editando = cliente
        
        # Campos del formulario
        fields = [
            ('ID_Cliente', 'ID Cliente:', 0),
            ('Nombre', 'Nombre:', 1),
            ('Apellido', 'Apellido:', 2),
            ('Telefono', 'Teléfono:', 3),
            ('Correo', 'Email:', 4),
            ('Direccion', 'Dirección:', 5)
        ]
        
        self.entries = {}
        for field, label, row in fields:
            ttk.Label(self.dialog, text=label).grid(row=row, column=0, padx=5, pady=5, sticky=tk.E)
            entry = ttk.Entry(self.dialog, width=30)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries[field] = entry
        
        # Si estamos editando, cargar los datos
        if cliente:
            self.entries['ID_Cliente'].insert(0, cliente[0])
            self.entries['ID_Cliente'].config(state='readonly')
            self.entries['Nombre'].insert(0, cliente[1] or "")
            self.entries['Apellido'].insert(0, cliente[2] or "")
            self.entries['Telefono'].insert(0, cliente[3] or "")
            self.entries['Correo'].insert(0, cliente[4] or "")
            self.entries['Direccion'].insert(0, cliente[5] or "")
        
        # Botones del diálogo
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Guardar", command=self.save_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def save_cliente(self):
        """Guarda los datos del cliente (creación o actualización)"""
        try:
            cliente_data = {
                'ID_Cliente': self.entries['ID_Cliente'].get(),
                'Nombre': self.entries['Nombre'].get(),
                'Apellido': self.entries['Apellido'].get() or None,
                'Telefono': self.entries['Telefono'].get() or None,
                'Correo': self.entries['Correo'].get() or None,
                'Direccion': self.entries['Direccion'].get() or None
            }
            
            if not cliente_data['Nombre']:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            db = SessionLocal()
            
            if self.cliente_editando:  # Actualizar
                cliente = db.query(Cliente).filter_by(ID_Cliente=cliente_data['ID_Cliente']).first()
                if cliente:
                    cliente.Nombre = cliente_data['Nombre']
                    cliente.Apellido = cliente_data['Apellido']
                    cliente.Telefono = cliente_data['Telefono']
                    cliente.Correo = cliente_data['Correo']
                    cliente.Direccion = cliente_data['Direccion']
                    db.commit()
                    messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            else:  # Crear nuevo
                nuevo_cliente = Cliente(**cliente_data)
                db.add(nuevo_cliente)
                db.commit()
                messagebox.showinfo("Éxito", "Cliente creado correctamente")
            
            self.load_clientes()
            self.dialog.destroy()
            
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo guardar el cliente: {str(e)}")
        finally:
            db.close()
    
    def edit_cliente(self, event):
        """Abre el diálogo de edición para el cliente seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un cliente")
            return
        
        item = self.tree.item(selected[0])
        self.open_add_dialog(item['values'])
    
    def delete_cliente(self):
        """Elimina el cliente seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un cliente")
            return
        
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            return
        
        item = self.tree.item(selected[0])
        cliente_id = item['values'][0]
        
        try:
            db = SessionLocal()
            cliente = db.query(Cliente).filter_by(ID_Cliente=cliente_id).first()
            if cliente:
                db.delete(cliente)
                db.commit()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.load_clientes()
            else:
                messagebox.showerror("Error", "No se encontró el cliente")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo eliminar el cliente: {str(e)}")
        finally:
            db.close()