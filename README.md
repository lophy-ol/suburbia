🚀 Sistema de Gestión CRUD - Padrino

[Python 3.8+] [MySQL 8.0] [Tkinter GUI]

📦 REQUISITOS PREVIOS
- Python 3.8 o superior
- MySQL Server 8.0+
- Git (opcional)

🛠️ INSTALACIÓN PASO A PASO

1. Clonar el repositorio:
git clone https://github.com/tu-usuario/suburbia.git
cd suburbia-main

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

📌 EJEMPLO DE CONEXIÓN A BASE DE DATOS (mysql.connector)

El sistema utiliza `mysql.connector` para conectarse a la base de datos MySQL. A continuación, un ejemplo de conexión:

```python
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # Carga variables desde el archivo .env

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM clientes")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
