import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.exc import SQLAlchemyError
from conexion import SessionLocal
from models import Caja  # Asegúrate de tener este modelo definido
from datetime import datetime

class CajaFrame(ttk.Frame):
    def __init__(self, parent, return_callback):
        super().__init__(parent)
        self.return_callback = return_callback
        self.create_widgets()
        self.load_cajas()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=5)

        ttk.Button(top_frame, text="Volver", command=self.return_callback).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Agregar Caja", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)

        columns = ['ID', 'Saldo Inicial', 'Fecha Apertura', 'Saldo Final', 'Fecha Cierre']
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<Double-1>', self.edit_caja)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Editar", command=lambda: self.edit_caja(None)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_caja).pack(side=tk.LEFT, padx=5)

    def load_cajas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            db = SessionLocal()
            cajas = db.query(Caja).order_by(Caja.fecha_apertura.desc()).all()

            for c in cajas:
                self.tree.insert('', tk.END, values=(
                    c.idcaja,
                    f"{c.saldo_inicial:.2f}",
                    c.fecha_apertura.strftime("%Y-%m-%d %H:%M"),
                    f"{c.saldo_final:.2f}",
                    c.fecha_cierre.strftime("%Y-%m-%d %H:%M")
                ))
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo cargar cajas: {str(e)}")
        finally:
            db.close()

    def open_add_dialog(self, caja=None):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Editar Caja" if caja else "Agregar Caja")
        self.dialog.grab_set()

        self.caja_editando = caja

        campos = [
            ('idcaja', 'ID:', 0),
            ('saldo_inicial', 'Saldo Inicial:', 1),
            ('fecha_apertura', 'Fecha Apertura (YYYY-MM-DD HH:MM):', 2),
            ('saldo_final', 'Saldo Final:', 3),
            ('fecha_cierre', 'Fecha Cierre (YYYY-MM-DD HH:MM):', 4)
        ]

        self.entries = {}
        for campo, label, fila in campos:
            ttk.Label(self.dialog, text=label).grid(row=fila, column=0, padx=5, pady=5, sticky=tk.E)
            entry = ttk.Entry(self.dialog, width=30)
            entry.grid(row=fila, column=1, padx=5, pady=5)
            self.entries[campo] = entry

        if caja:
            self.entries['idcaja'].insert(0, caja[0])
            self.entries['idcaja'].config(state='readonly')
            self.entries['saldo_inicial'].insert(0, caja[1])
            self.entries['fecha_apertura'].insert(0, caja[2])
            self.entries['saldo_final'].insert(0, caja[3])
            self.entries['fecha_cierre'].insert(0, caja[4])

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self.save_caja).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)

    def save_caja(self):
        try:
            data = {
                'idcaja': self.entries['idcaja'].get(),
                'saldo_inicial': self.entries['saldo_inicial'].get(),
                'fecha_apertura': self.entries['fecha_apertura'].get(),
                'saldo_final': self.entries['saldo_final'].get(),
                'fecha_cierre': self.entries['fecha_cierre'].get()
            }

            db = SessionLocal()

            if self.caja_editando:
                c = db.query(Caja).filter_by(idcaja=data['idcaja']).first()
                if c:
                    c.saldo_inicial = float(data['saldo_inicial'])
                    c.fecha_apertura = datetime.strptime(data['fecha_apertura'], "%Y-%m-%d %H:%M")
                    c.saldo_final = float(data['saldo_final'])
                    c.fecha_cierre = datetime.strptime(data['fecha_cierre'], "%Y-%m-%d %H:%M")
                    db.commit()
                    messagebox.showinfo("Éxito", "Caja actualizada")
            else:
                nueva = Caja(
                    saldo_inicial=float(data['saldo_inicial']),
                    fecha_apertura=datetime.strptime(data['fecha_apertura'], "%Y-%m-%d %H:%M"),
                    saldo_final=float(data['saldo_final']),
                    fecha_cierre=datetime.strptime(data['fecha_cierre'], "%Y-%m-%d %H:%M")
                )
                db.add(nueva)
                db.commit()
                messagebox.showinfo("Éxito", "Caja agregada")

            self.load_cajas()
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la caja: {str(e)}")
        finally:
            db.close()

    def edit_caja(self, event):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una caja")
            return

        item = self.tree.item(selected[0])
        self.open_add_dialog(item['values'])

    def delete_caja(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una caja")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta caja?"):
            return

        caja_id = self.tree.item(selected[0])['values'][0]

        try:
            db = SessionLocal()
            caja = db.query(Caja).filter_by(idcaja=caja_id).first()
            if caja:
                db.delete(caja)
                db.commit()
                messagebox.showinfo("Éxito", "Caja eliminada")
                self.load_cajas()
            else:
                messagebox.showerror("Error", "No se encontró la caja")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
        finally:
            db.close()
