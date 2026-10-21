# aws-academy


---

```markdown
# 🚀 Data Engineering Labs & ETL Pipelines (AWS S3 & PostgreSQL)

Repositorio oficial que contiene el desarrollo de prácticas y pipelines de ingeniería de datos, modelado multidimensional (Data Warehouse / Esquemas Estrella) y automatización ETL utilizando **Python**, **Pandas**, **scikit-learn**, **Boto3**, **SQLAlchemy** y **PostgreSQL**, desplegado sobre una instancia **AWS EC2 (Ubuntu)**.

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

Desarrollado como parte de las prácticas académicas de la carrera de **Ingeniería en Desarrollo y Gestión de Software (IDyGS)**.

```

```
