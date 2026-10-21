import io
import json
import os
import boto3
import pandas as pd
import yaml
from botocore.exceptions import ClientError
from sqlalchemy import create_engine

def cargar_configuracion(nombre_archivo="config.yaml"):
    """Carga los parámetros usando la ruta absoluta del directorio del script."""
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    path_config = os.path.join(dir_actual, nombre_archivo)

    with open(path_config, "r") as file:
        return yaml.safe_load(file)

config = cargar_configuracion()

AWS_REGION = config["aws"]["region"]
BUCKET_NAME = config["aws"]["bucket_name"]

s3_client = boto3.client("s3", region_name=AWS_REGION)

pg_conf = config["postgres"]
db_nombre = pg_conf["databases"]["laboratorios"]

db_url = (
    f"postgresql+psycopg://{pg_conf['user']}:{pg_conf['password']}"
    f"@{pg_conf['host']}:{pg_conf['port']}/{db_nombre}"
)

def cargar_y_perfilar_s3(file_key, is_json=False):
    """Descarga archivos desde S3 y genera un perfilamiento básico de tipos de datos."""
    print(f"\n=== Procesando objeto S3: {file_key} ===")
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
        body = response["Body"].read()

        if is_json:
            data_json = json.loads(body.decode("utf-8"))
            df = pd.json_normalize(data_json)
        else:
            df = pd.read_csv(io.BytesIO(body))

        print(
            f"Dimensiones del dataset: {df.shape[0]} filas x {df.shape[1]} columnas"
        )
        print("\nPerfil de Tipos de Datos e Identificación de Tipos:")
        print(df.dtypes)
        print("\nResumen de Estadísticos Descriptivos (Cuantitativos):")
        print(df.describe().T)

        return df

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            print(
                f"⚠️ Error: La clave '{file_key}' no existe en el bucket '{BUCKET_NAME}'."
            )
            print("Objetos disponibles en el bucket:")

            objects = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
            if "Contents" in objects:
                for obj in objects["Contents"]:
                    print(f"  - {obj['Key']}")
            else:
                print("  (El bucket está vacío)")
            return None
        else:
            raise e


def guardar_en_postgres(df, nombre_tabla):
    """Guarda el DataFrame perfilado en la base de datos laboratorios_db."""
    if df is None:
        print(
            f"⚠️ Omitiendo carga en PostgreSQL: DataFrame nulo para la tabla '{nombre_tabla}'."
        )
        return

    try:
        engine = create_engine(db_url)
        df.to_sql(
            name=nombre_tabla,
            con=engine,
            if_exists="replace",
            index=False,
        )
        print(
            f"-> Éxito: Datos guardados en la tabla '{nombre_tabla}' de PostgreSQL ({db_nombre})."
        )
    except Exception as e:
        print(f"Error al guardar en PostgreSQL: {e}")


if __name__ == "__main__":
        df_transacciones = cargar_y_perfilar_s3("raw/transacciones.csv")
    df_logs = cargar_y_perfilar_s3("raw/logs_m2m.json", is_json=True)

    guardar_en_postgres(df_transacciones, "transacciones_p1")
    guardar_en_postgres(df_logs, "logs_m2m_p1")