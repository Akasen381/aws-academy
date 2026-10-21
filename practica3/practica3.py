import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

# Generación de dataset con ruido sintético
data = {
    "edad": [
        25,
        30,
        np.nan,
        45,
        22,
        120,
        35,
        28,
        np.nan,
        40,
    ],  # 120 es atípico/erróneo
    "ingreso_mensual": [
        15000,
        22000,
        18000,
        np.nan,
        12000,
        950000,
        25000,
        21000,
        19000,
        np.nan,
    ],  # 950k outlier
    "scoring_credito": [650, 700, 680, 710, 590, 800, 670, 640, 620, 730],
}

df_dirty = pd.DataFrame(data)

# 1. Tratamiento de Valores Atípicos por IQR sobre 'ingreso_mensual'
Q1 = df_dirty["ingreso_mensual"].quantile(0.25)
Q3 = df_dirty["ingreso_mensual"].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR

print(f"Límite Superior para Outliers en Ingreso: ${limite_superior:,.2f}")

# Reemplazar outliers extremos con NaN para tratarlos en la imputación
df_dirty.loc[
    df_dirty["ingreso_mensual"] > limite_superior, "ingreso_mensual"
] = np.nan

# Corrección de valor erróneo de regla de negocio (Edad > 100)
df_dirty.loc[df_dirty["edad"] > 100, "edad"] = np.nan

# 2. Imputación Múltiple Avanzada con KNNImputer (k=2)
imputer = KNNImputer(n_neighbors=2)
df_clean_array = imputer.fit_transform(df_dirty)

# Reconstruir el DataFrame preservando los nombres de las columnas
df_clean = pd.DataFrame(df_clean_array, columns=df_dirty.columns)

print("\n=== DATASET LIMPIO E IMPUTADO ===")
print(df_clean)