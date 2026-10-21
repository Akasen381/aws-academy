# aws-academy


---

```markdown
# 🚀 Data Engineering Labs & ETL Pipelines (AWS S3 & PostgreSQL)

---

## 📂 Estructura del Proyecto

El repositorio está organizado de forma modular, desacoplando las credenciales y parámetros de conexión mediante un archivo de configuración centralizado (`config.yaml`).

```text
.
├── config.yaml          # Parámetros globales de AWS y PostgreSQL (No versionado en git público)
├── practica1.py         # Perfilamiento e ingesta multi-fuente desde AWS S3
├── practica2.py         # Modelado multidimensional y carga de Esquema Estrella
├── pipeline.py          # Pipeline ETL automatizado (MinMaxScaler, Binning, Parquet a S3)
├── requirements.txt     # Dependencias del proyecto Python
└── README.md            # Documentación general del repositorio

```

---

## 🛠️ Requisitos Técnicos y Entorno

* **Sistema Operativo:** Ubuntu 22.04+ (AWS EC2 / AWS Academy)
* **Base de Datos:** PostgreSQL 18+
* **Lenguaje:** Python 3.10+
* **Librerías Principales:** `pandas`, `numpy`, `scikit-learn`, `boto3`, `sqlalchemy`, `psycopg`, `pyyaml`, `pyarrow`

### Instalación de Dependencias

1. Activa tu entorno virtual de Python:
```bash
source pipeline/bin/activate  # O tu entorno activo (venv / conda)

```


2. Instala las librerías requeridas:
```bash
pip install -r requirements.txt

```



---

## ⚙️ Configuración del Entorno (`config.yaml`)

Crea un archivo llamado `config.yaml` en la raíz del proyecto para gestionar las credenciales y bases de datos de forma segura:

```yaml
postgres:
  user: "xxxxxxxx"
  password: "mi_passwordxxx"
  host: "localhost"
  port: xxxx
  databases:
    laboratorios: "xxxxxxxxx_db"  # Para Prácticas 1, 2, 3 y 4
    practica5: "xxxxxxxx_db"         # Exclusivo para Pipeline ETL (Práctica 5)

aws:
  region: "us-east-1"
  bucket_name: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

```

---

## 🗄️ Arquitectura de Bases de Datos (Aislamiento de Entornos)

El proyecto separa lógicamente los entornos operacionales para evitar conflictos entre prácticas:

| Base de datos PostgreSQL | Prácticas Asociadas | Tablas Generadas |
| --- | --- | --- |
| **`laboratorios_db`** | Prácticas 1, 2, 3, 4 | `transacciones_p1`, `logs_m2m_p1`, `dim_cliente`, `dim_producto`, `dim_tiempo`, `fact_ventas` |
| **`practica_db`** | Práctica 5 (ETL Pipeline) | `clientes_transformados` |

---

## 🚀 Ejecución de los Scripts

### 1. Práctica 1: Perfilamiento e Ingesta desde S3

Descarga archivos estructurados (`.csv`) y semiestructurados (`.json`) desde el bucket de AWS S3, genera estadísticas descriptivas y persiste los resultados en `laboratorios_db`.

```bash
python practica1.py

```

### 2. Práctica 2: Esquema Estrella (Data Warehouse)

Simula una ingesta OLTP, separa los datos dimensionales generando **Claves Subrogadas (Surrogate Keys)**, calcula la tabla de hechos (`fact_ventas`) con métricas agregadas y carga el modelo relacional completo en `laboratorios_db`.

```bash
python practica2.py

```

### 3. Práctica 5: Pipeline ETL Automatizado (Parquet & S3)

Ejecuta la extracción de datos, aplica discretización (`pd.cut`), normalización de características (`MinMaxScaler`), genera un búfer en memoria serializado en formato comprimido **Apache Parquet**, lo sube a la zona `processed/` de AWS S3 y carga la tabla en `practica_db`.

```bash
python pipeline.py

```

---

## 🔒 Buenas Prácticas de Control de Versiones (`.gitignore`)

Para proteger las credenciales institucionales y evitar la exposición de tokens temporales de AWS Academy, el archivo `.gitignore` debe incluir:

```text
# Entornos virtuales
venv/
env/
pipeline/

# Credenciales y archivos de configuración sensibles
config.yaml
.aws/
credentials

# Caché de Python
__pycache__/
*.pyc

```

---

## 👨‍💻 Autor

---

### 1. Configuración de AWS CLI y Credenciales

Para asegurar que tu instancia se conecte correctamente al bucket de AWS S3 y utilice las credenciales temporales:

```bash
# Verificar la instalación o versión de la CLI de AWS
aws --version

# Configurar credenciales y región por defecto (us-east-1)
aws configure


---

### 1. Configuración y Credenciales

* **Configurar credenciales y región inicial:**
```bash
aws configure

```


*(Te pedirá tu `AWS Access Key ID`, `AWS Secret Access Key`, región por defecto como `us-east-1` y formato de salida).*
* **Verificar la identidad del usuario actual:**
```bash
aws sts get-caller-identity

```


* **Ver la configuración activa:**
```bash
aws configure list

```



---

### 2. Comandos para Amazon S3 (Almacenamiento)

* **Listar todos tus buckets:**
```bash
aws s3 ls

```


* **Listar el contenido (archivos y carpetas) dentro de un bucket específico:**
```bash
aws s3 ls s3://nombre-del-bucket/

```


* **Subir un archivo local a S3:**
```bash
aws s3 cp archivo.txt s3://nombre-del-bucket/carpeta/

```


* **Descargar un archivo desde S3 a tu máquina local:**
```bash
aws s3 cp s3://nombre-del-bucket/carpeta/archivo.txt .

```


* **Sincronizar una carpeta local completa con un bucket en S3 (muy útil para respaldos):**
```bash
aws s3 sync ./mi-carpeta s3://nombre-del-bucket/mi-carpeta/

```


* **Eliminar un archivo en S3:**
```bash
aws s3 rm s3://nombre-del-bucket/archivo.txt

```



---

### 3. Comandos para Amazon EC2 (Instancias y Servidores)

* **Listar tus instancias EC2 y su estado actual:**
```bash
aws ec2 describe-instances

```


* **Filtrar el estado de las instancias (ej. ver solo las que están en ejecución):**
```bash
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"

```



---

¿Hay algún servicio o tarea específica de AWS que necesites automatizar o consultar en este momento?
```

*(También puedes verificar o editar manualmente las credenciales en `~/.aws/credentials`)*.

---

### 2. Creación y Activación del Entorno Virtual de Python

Para mantener aisladas las librerías del proyecto:

```bash
# Crear el entorno virtual llamado 'venv' (o 'pipeline')
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate

```

---

### 3. Instalación de Dependencias del Proyecto

Una vez activo el entorno virtual, instala las librerías necesarias (`boto3`, `pandas`, `sqlalchemy`, `scikit-learn`, `faker`, etc.):

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar todas las dependencias principales del proyecto
pip install boto3 pandas numpy pyyaml sqlalchemy psycopg2-binary scikit-learn faker matplotlib seaborn

# (O si ya cuentas con un archivo de requerimientos)
pip install -r requirements.txt

```

---

### 4. Configuración y Servicio de PostgreSQL (`laboratorios_db`)

Si necesitas gestionar el servicio local de la base de datos en tu instancia EC2:

```bash
# Actualizar paquetes e instalar PostgreSQL y cliente
sudo apt update && sudo apt install postgresql postgresql-contrib -y

# Iniciar y habilitar el servicio de PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Acceder a la consola de PostgreSQL como usuario postgres
sudo -u postgres psql

# Comandos útiles dentro de psql para crear la base de datos:
# CREATE DATABASE laboratorios_db;
# \l  (para listar bases de datos)
# \q  (para salir)

```

---



```

```

```
