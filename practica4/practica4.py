import numpy as np
import pandas as pd
from faker import Faker
from sklearn.model_selection import train_test_split

# Inicializar Faker con localización en español (México) y fijar semillas para reproducibilidad
fake = Faker("es_MX")
Faker.seed(42)
np.random.seed(42)

# 1. Generación programática de dataset sintético con Faker (1,000 registros)
registros = []
for i in range(1000):
    registros.append({
        "id_cliente": i + 1,
        "nombre": fake.name(),
        "email": fake.email(),
        "estado_civil": np.random.choice(
            ["Soltero", "Casado", "Divorciado"], p=[0.5, 0.4, 0.1]
        ),
        "ingreso_anual": round(np.random.uniform(100000, 1000000), 2),
        "churn": np.random.choice([0, 1], p=[0.8, 0.2]),  # 20% tasa de abandono
    })

df_sintetico = pd.DataFrame(registros)

# 2. Selección de Datos Objetivo (Target) y Características (Features)
# Se excluyen variables de identificador único (id, nombre, email) para evitar sobreajuste
X = df_sintetico.drop(columns=["id_cliente", "nombre", "email", "churn"])
y = df_sintetico["churn"]

# 3. Partición Estratificada (Train 80%, Test 20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Impresión de resultados
print(
    f"Dimensiones Train Set: {X_train.shape} | Proporción Churn: {y_train.mean():.2f}"
)
print(
    f"Dimensiones Test Set:  {X_test.shape} | Proporción Churn: {y_test.mean():.2f}"
)