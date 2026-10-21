import io
import boto3
import pandas as pd
import yaml
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine


# 1. Función para cargar la configuración modular
def cargar_configuracion(path="config.yaml"):
    """Carga los parámetros de AWS y PostgreSQL desde el archivo YAML."""
    with open(path, "r") as file:
        return yaml.safe_load(file)


def pipeline_etl_completo():
    print("=== Carga de Configuración ===")
    config = cargar_configuracion("config.yaml")

    # Credenciales y Parámetros
    BUCKET_NAME = config["aws"]["bucket_name"]
    AWS_REGION = config["aws"]["region"]

    pg = config["postgres"]
    # Selecciona la base de datos exclusiva para la Práctica 5
    db_nombre = pg["databases"]["practica5"]
    db_url = f"postgresql+psycopg://{pg['user']}:{pg['password']}@{pg['host']}:{pg['port']}/{db_nombre}"

    print("\n=== 1. FASE DE EXTRACCIÓN (Extract) ===")
    raw_data = {
        "cliente": ["A", "B", "C", "D"],
        "edad": [20, 40, 60, 30],
        "monto_compras": [1200.0, 50000.0, 30000.0, 15000.0],
    }
    df_raw = pd.DataFrame(raw_data)

    print("=== 2. FASE DE TRANSFORMACIÓN (Transform) ===")
    df_raw["categoria_edad"] = pd.cut(
        df_raw["edad"],
        bins=[0, 25, 50, 100],
        labels=["Joven", "Adulto", "Senior"],
    )

    scaler = MinMaxScaler()
    df_raw["monto_normalizado"] = scaler.fit_transform(
        df_raw[["monto_compras"]]
    )
    df_raw["score_promocional"] = df_raw["monto_normalizado"] * 100

    print("Dataset Transformado:")
    print(df_raw)

    print("\n=== 3. FASE DE CARGA (Load) ===")

    # --- 3A. CARGA A AWS S3 ---
    buffer = io.BytesIO()
    df_raw.to_parquet(buffer, index=False)
    buffer.seek(0)

    s3_client = boto3.client("s3", region_name=AWS_REGION)

    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key="processed/etl_output.parquet",
            Body=buffer.getvalue(),
        )
        print(
            f"-> Éxito: Archivo Parquet cargado en s3://{BUCKET_NAME}/processed/etl_output.parquet"
        )
    except Exception as e:
        print(f"Error al subir a S3: {e}")

    # --- 3B. CARGA A POSTGRESQL ---
    try:
        engine = create_engine(db_url)

        # Cargar DataFrame a la tabla 'clientes_transformados' en 'practica_db'
        df_raw.to_sql(
            name="clientes_transformados",
            con=engine,
            if_exists="replace",
            index=False,
        )
        print(
            f"-> Éxito: Datos cargados correctamente en la tabla 'clientes_transformados' de PostgreSQL ({db_nombre})."
        )
    except Exception as e:
        print(f"Error al cargar en PostgreSQL: {e}")


if __name__ == "__main__":
    pipeline_etl_completo()