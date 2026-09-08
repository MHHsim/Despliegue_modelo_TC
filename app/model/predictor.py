import os
import joblib
import numpy as np
import pandas as pd

# ---------------------------------------------------------
# 1. Carga de modelos
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)

def load_artifact(name):
    """Carga artefactos desde app/model/"""
    path = os.path.join(BASE_DIR, name)
    return joblib.load(path)

# Pipeline completo entrenado
final_model = load_artifact("model_bank_marketing.pkl")

# Modelos de segmentación
scaler_segmentacion = load_artifact("scaler_segmentacion.pkl")
kmeans_segmentacion = load_artifact("kmeans_segmentacion.pkl")

# Variables usadas para segmentación
SEGMENT_FEATS = [
    "age",
    "log_balance",
    "campaign",
    "previous",
    "housing_b",
    "loan_b",
    "contacted_before"
]

# ---------------------------------------------------------
# 2. Función para asignar segmento
# ---------------------------------------------------------

def asignar_segmento(datos):
    """
    Recibe un dict con los datos del cliente.
    Devuelve el segmento KMeans.
    """
    d = datos.copy()

    # Variables derivadas
    d["log_balance"] = np.sign(d["balance"]) * np.log1p(abs(d["balance"]))
    d["housing_b"] = 1 if d["housing"] == "yes" else 0
    d["loan_b"] = 1 if d["loan"] == "yes" else 0
    d["contacted_before"] = 1 if d["pdays"] != -1 else 0

    # Crear DataFrame con las variables del cluster
    df_cluster = pd.DataFrame([{
        feat: d[feat] for feat in SEGMENT_FEATS
    }])

    # Escalar y predecir segmento
    scaled = scaler_segmentacion.transform(df_cluster)
    segmento = int(kmeans_segmentacion.predict(scaled)[0])

    return segmento

# ---------------------------------------------------------
# 3. Función principal de predicción
# ---------------------------------------------------------

def predict(input_dict):
    """
    Recibe un dict con los datos del cliente.
    Devuelve:
        - segment
        - prediction (0/1)
        - probability (float)
    """

    # 1) Asignar segmento
    segmento = asignar_segmento(input_dict)

    # 2) Preparar DataFrame para el pipeline
    df = pd.DataFrame([input_dict])
    df["segment"] = segmento

    # 3) Predicción con el pipeline completo
    pred = int(final_model.predict(df)[0])
    prob = float(final_model.predict_proba(df)[0][1])

    return {
        "segment": segmento,
        "prediction": pred,
        "probability": round(prob, 4)
    }

print("Tipo de modelo cargado:", type(final_model))
