import os
import numpy as np
import pandas as pd
import yaml
from sqlalchemy import create_engine


# 1. Cargar la configuración modular desde config.yaml
def cargar_configuracion(nombre_archivo="config.yaml"):
    """Carga la configuración YAML resolviendo la ruta absoluta del directorio actual."""
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    path_config = os.path.join(dir_actual, nombre_archivo)

    with open(path_config, "r") as file:
        return yaml.safe_load(file)


# Cargar parámetros
config = cargar_configuracion()
pg_conf = config["postgres"]
db_nombre = pg_conf["databases"]["laboratorios"]  # Apunta a 'laboratorios_db'

db_url = (
    f"postgresql+psycopg://{pg_conf['user']}:{pg_conf['password']}"
    f"@{pg_conf['host']}:{pg_conf['port']}/{db_nombre}"
)

# 2. Simulación de Ingesta Operativa (OLTP)
np.random.seed(101)
n = 500
df_operativo = pd.DataFrame({
    "id_transaccion": range(1000, 1000 + n),
    "fecha_hora": pd.date_range(start="2026-01-01", periods=n, freq="h"),
    "cliente_nombre": np.random.choice(
        ["Juan Pérez", "María Gómez", "Carlos Ruiz"], n
    ),
    "cliente_ciudad": np.random.choice(
        ["Puebla", "CDMX", "Guadalajara"], n
    ),
    "producto_nombre": np.random.choice(
        ["Laptop Dell", "Mouse Logi", "Monitor LG"], n
    ),
    "categoria_prod": np.random.choice(
        ["Cómputo", "Accesorios", "Pantallas"], n
    ),
    "precio_unitario": np.random.choice([15000.0, 350.0, 4500.0], n),
    "cantidad": np.random.randint(1, 5, n),
})

# 3. Construcción de Dimensión Cliente (Dim_Cliente)
dim_cliente = (
    df_operativo[["cliente_nombre", "cliente_ciudad"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_cliente["id_cliente_sk"] = dim_cliente.index + 1  # Surrogate Key

# 4. Construcción de Dimensión Producto (Dim_Producto)
dim_producto = (
    df_operativo[["producto_nombre", "categoria_prod", "precio_unitario"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_producto["id_producto_sk"] = dim_producto.index + 1

# 5. Construcción de Dimensión Tiempo (Dim_Tiempo)
dim_tiempo = pd.DataFrame(
    {"fecha_completa": df_operativo["fecha_hora"].dt.date.unique()}
)
dim_tiempo["fecha_completa"] = pd.to_datetime(dim_tiempo["fecha_completa"])
dim_tiempo["id_tiempo_sk"] = (
    dim_tiempo["fecha_completa"].dt.strftime("%Y%m%d").astype(int)
)
dim_tiempo["anio"] = dim_tiempo["fecha_completa"].dt.year
dim_tiempo["mes"] = dim_tiempo["fecha_completa"].dt.month
dim_tiempo["dia"] = dim_tiempo["fecha_completa"].dt.day

# 6. Construcción de la Tabla de Hechos (Fact_Ventas)
fact_ventas = df_operativo.merge(
    dim_cliente, on=["cliente_nombre", "cliente_ciudad"]
).merge(
    dim_producto, on=["producto_nombre", "categoria_prod", "precio_unitario"]
)

fact_ventas["fecha_completa"] = pd.to_datetime(
    fact_ventas["fecha_hora"].dt.date
)
fact_ventas = fact_ventas.merge(dim_tiempo, on="fecha_completa")
fact_ventas["monto_total"] = (
    fact_ventas["cantidad"] * fact_ventas["precio_unitario"]
)

# Selección final de columnas para la Fact Table
fact_table = fact_ventas[[
    "id_transaccion",
    "id_cliente_sk",
    "id_producto_sk",
    "id_tiempo_sk",
    "cantidad",
    "monto_total",
]]

print("=== TABLA DE HECHOS (FACT_VENTAS) ===")
print(fact_table.head())

try:
    engine = create_engine(db_url)

    dim_cliente.to_sql(
        name="dim_cliente", con=engine, if_exists="replace", index=False
    )
    dim_producto.to_sql(
        name="dim_producto", con=engine, if_exists="replace", index=False
    )
    dim_tiempo.to_sql(
        name="dim_tiempo", con=engine, if_exists="replace", index=False
    )

    fact_table.to_sql(
        name="fact_ventas", con=engine, if_exists="replace", index=False
    )

    print(
        f"\n-> Éxito: Esquema Estrella cargado en PostgreSQL ({db_nombre})."
    )
except Exception as e:
    print(f"\nError al guardar en PostgreSQL: {e}")