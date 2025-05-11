import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

# Configuración de módulos con colores e íconos
MODULOS = {
    "Clientes": {"icono": "👥", "color": "#3498db", "texto": "white"},
    "Proveedores": {"icono": "📦", "color": "#2ecc71", "texto": "white"},
    "Productos": {"icono": "🛍️", "color": "#e74c3c", "texto": "white"},
    "Empleados": {"icono": "👨‍💼", "color": "#f39c12", "texto": "white"},
    "Ventas": {"icono": "💰", "color": "#9b59b6", "texto": "white"},
    "Sucursales": {"icono": "🏬", "color": "#1abc9c", "texto": "white"},
    "Reportes": {"icono": "📊", "color": "#34495e", "texto": "white"},
    "Caja": {"icono": "💵", "color": "#e67e22", "texto": "white"},
    "Métodos de Pago": {"icono": "💳", "color": "#27ae60", "texto": "white"}
}

def crear_dashboard(root, navegadores_modulos):
    # Configurar fuente personalizada
    fuente_titulo = Font(family="Helvetica", size=18, weight="bold")
    fuente_botones = Font(family="Arial", size=12, weight="bold")
    
    # Frame principal con fondo claro
    main_frame = tk.Frame(root, bg="#f5f6fa")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Título del dashboard
    titulo_frame = tk.Frame(main_frame, bg="#f5f6fa")
    titulo_frame.pack(pady=(0, 30))
    
    tk.Label(
        titulo_frame, 
        text="📊 Panel de Control", 
        font=fuente_titulo,
        bg="#f5f6fa",
        fg="#2c3e50"
    ).pack()
    
    tk.Label(
        titulo_frame, 
        text="Seleccione un módulo", 
        font=("Arial", 12),
        bg="#f5f6fa",
        fg="#7f8c8d"
    ).pack()
    
    # Contenedor de botones con grid flexible
    botones_frame = tk.Frame(main_frame, bg="#f5f6fa")
    botones_frame.pack(fill=tk.BOTH, expand=True)
    
    # Calcular número de filas necesarias (3 columnas)
    num_modulos = len(navegadores_modulos)
    num_filas = (num_modulos + 2) // 3  # Redondeo hacia arriba
    
    # Configurar grid responsivo
    for i in range(3):
        botones_frame.columnconfigure(i, weight=1, uniform="cols")
    for j in range(num_filas):
        botones_frame.rowconfigure(j, weight=1, uniform="rows")
    
    # Crear botones para cada módulo
    for index, (modulo, accion) in enumerate(navegadores_modulos.items()):
        datos = MODULOS.get(modulo, {"icono": "🔘", "color": "#95a5a6", "texto": "white"})
        
        fila = index // 3
        columna = index % 3
        
        btn = tk.Button(
            botones_frame,
            text=f"{datos['icono']} {modulo}",
            font=fuente_botones,
            bg=datos["color"],
            fg=datos["texto"],
            activebackground=datos["color"],
            activeforeground=datos["texto"],
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=15,
            command=accion
        )
        
        # Efecto hover
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2c3e50"))
        btn.bind("<Leave>", lambda e, b=btn, c=datos["color"]: b.config(bg=c))
        
        btn.grid(
            row=fila, 
            column=columna, 
            padx=10, 
            pady=10, 
            sticky="nsew"
        )
    
    return main_frame