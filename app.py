import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from cliente import ClienteFrame  
from almacen import AlmacenFrame  
from caja import CajaFrame  
from metodo_de_pago import MetodoPagoFrame  
from proveedor import ProveedorFrame 
from sucursal import SucursalFrame  

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard de Gestión")
        self.root.geometry("700x500")
        self.root.configure(bg='#f5f5f5')
        
        # Configurar fuente
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight='bold')
        self.button_font = tkfont.Font(family='Helvetica', size=12)
        
        # Variable para controlar el frame actual
        self.current_frame = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Limpiar frame actual si existe
        if self.current_frame:
            self.current_frame.destroy()
        
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, 
                        text="Sistema de Gestión Comercial", 
                        font=self.title_font,
                        bg='#2c3e50',
                        fg='white')
        title.pack(side=tk.LEFT, padx=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f5f5f5')
        main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_frame = main_container
        
        # Dashboard cards
        cards_frame = tk.Frame(main_container, bg='#f5f5f5')
        cards_frame.pack(expand=True)
        
        # Opciones del dashboard
        options = [
            ("Almacén", "📦", "#3498db", self.open_almacen),
            ("Caja", "💵", "#2ecc71", self.open_caja),
            ("Clientes", "👥", "#e74c3c", self.open_cliente),
            ("Métodos de Pago", "💳", "#9b59b6", self.open_metodo_pago),
            ("Proveedores", "🚚", "#f39c12", self.open_proveedor),
            ("Sucursales", "🏢", "#1abc9c", self.open_sucursal)
        ]
        
        # Crear cards
        for i, (title, icon, color, command) in enumerate(options):
            row = i // 3
            col = i % 3
            
            card = tk.Frame(cards_frame, 
                           bg='white', 
                           relief=tk.RAISED, 
                           borderwidth=1,
                           padx=10, 
                           pady=10)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Icono
            icon_label = tk.Label(card, 
                                text=icon, 
                                font=("Arial", 24),
                                bg='white')
            icon_label.pack(pady=(10,5))
            
            # Título
            title_label = tk.Label(card, 
                                  text=title, 
                                  font=self.button_font,
                                  bg='white')
            title_label.pack(pady=(0,10))
            
            # Botón
            btn = tk.Button(card,
                          text="Acceder",
                          command=command,
                          bg=color,
                          fg='white',
                          activebackground=color,
                          activeforeground='white',
                          relief=tk.FLAT,
                          font=self.button_font)
            btn.pack(fill=tk.X, padx=5, pady=5)
            
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#34495e'))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
    
    # Funciones para las secciones
    def open_almacen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        almacen_Frame = AlmacenFrame(self.root, self.create_widgets)
        almacen_Frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.current_frame = almacen_Frame
            
    
    def open_caja(self):
        self.show_section("Caja", "💵")
        for widget in self.root.winfo_children():
            widget.destroy()
        
        caja_frame = CajaFrame(self.root, self.create_widgets)
        caja_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.current_frame = caja_frame
    
    def open_cliente(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        clientes_frame = ClienteFrame(self.root, self.create_widgets)
        clientes_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.current_frame = clientes_frame
    
    def open_metodo_pago(self):
        self.show_section("Métodos de Pago", "💳")
        for widget in self.root.winfo_children():
            widget.destroy()
        
        MetodoPagoFrame_frame = MetodoPagoFrame(self.root, self.create_widgets)
        MetodoPagoFrame_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.current_frame = MetodoPagoFrame_frame
    
    def open_proveedor(self):
        self.show_section("Proveedores", "🚚")
        for widget in self.root.winfo_children():
            widget.destroy()
        
        Proveedor_frame = ProveedorFrame(self.root, self.create_widgets)
        Proveedor_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.current_frame = Proveedor_frame
    
    def open_sucursal(self):
        self.show_section("Sucursales", "🏢")
        self.show_section("Proveedores", "🚚")
        for widget in self.root.winfo_children():
            widget.destroy()
        
        sucursal_Frame = SucursalFrame(self.root, self.create_widgets)
        sucursal_Frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.current_frame = sucursal_Frame
    
    def show_section(self, section_name, icon):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill=tk.X)
        
        back_btn = tk.Button(header,
                            text="⬅ Volver",
                            command=self.create_widgets,
                            bg='#34495e',
                            fg='white',
                            relief=tk.FLAT,
                            font=self.button_font)
        back_btn.pack(side=tk.LEFT, padx=10)
        
        title = tk.Label(header, 
                        text=f"{icon} {section_name}", 
                        font=self.title_font,
                        bg='#2c3e50',
                        fg='white')
        title.pack(side=tk.LEFT, padx=20)
        
        # Contenido
        content = tk.Frame(self.root, bg='#f5f5f5')
        content.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()