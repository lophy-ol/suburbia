🚀 Sistema de Gestión CRUD - Padrino

[Python 3.8+] [MySQL 8.0] [Tkinter GUI]

📦 REQUISITOS PREVIOS
- Python 3.8 o superior
- MySQL Server 8.0+
- Git (opcional)

🛠️ INSTALACIÓN PASO A PASO

1. Clonar el repositorio:
git clone https://github.com/tu-usuario/padrino-crud.git
cd padrino-crud

2. Configurar entorno virtual:
python -m venv 23270667

Para activar:
- Windows: 23270667\Scripts\activate
- Linux/MacOS: source 23270667/bin/activate

3. Instalar dependencias:
pip install -r requirements.txt

⚙️ CONFIGURACIÓN INICIAL

1. Copiar archivo de configuración:
cp .env.example .env

2. Editar .env con tus credenciales:
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=padrino_db

3. IMPORTAR LA BASE DE DATOS suburbia.sql:
- Método 1 (usando línea de comandos):
  mysql -u root -p padrino_db < suburbia.sql
  
- Método 2 (usando MySQL Workbench):
  1. Abrir MySQL Workbench
  2. Conectarse al servidor MySQL
  3. Click en "Server" > "Data Import"
  4. Seleccionar "Import from Self-Contained File"
  5. Buscar y seleccionar el archivo suburbia.sql
  6. Seleccionar el esquema padrino_db como destino
  7. Click en "Start Import"

🖥️ INICIAR EL SISTEMA
python app.py

🧩 MÓDULOS PRINCIPALES

Clientes      👥  Gestión de clientes
Proveedores   📦  Administración de proveedores
Productos     🛍️  Inventario de productos
Empleados     👨‍💼 Registro de personal
Ventas        💰  Procesos de ventas
Sucursales    🏬  Administración de locales
Reportes      📊  Generación de informes

📌 CARACTERÍSTICAS CLAVE
- Interfaz moderna con Tkinter
- Diseño responsive
- Validación de datos integrada
- Búsqueda avanzada
- Exportación a PDF/Excel
- Dashboard interactivo

🐛 SOLUCIÓN DE PROBLEMAS COMUNES
Error con tkcalendar:
pip install --upgrade pip
pip install tkcalendar

Error de conexión MySQL:
1. Verificar que el servicio MySQL esté corriendo
2. Revisar credenciales en .env
3. Asegurar privilegios suficientes
4. Confirmar que la base de datos suburbia.sql se importó correctamente

📄 ESTRUCTURA DEL PROYECTO
padrino-crud/
├── app.py                # Punto de entrada
├── init_db.py            # Inicialización de BD
├── requirements.txt      # Dependencias
├── .env.example          # Plantilla configuración
├── suburbia.sql          # Base de datos completa
├── controllers/          # Lógica de negocio
├── models/               # Modelos de datos
├── views/                # Interfaces
│   ├── components/       # Componentes UI
│   └── styles/           # Estilos CSS
├── utils/                # Helpers
└── docs/                 # Documentación