import pickle
import pandas as pd

# -----------------------------
# 1. Cargar scaler, modelo de segmentación y modelo final
# -----------------------------

def load_scaler():
    with open("app/model/scaler_segmentacion.pkl", "rb") as f:
        scaler = pickle.load(f)
    return scaler

def load_segment_model():
    with open("app/model/kmeans_segmentacion.pkl", "rb") as f:
        model = pickle.load(f)
    return model

def load_final_model():
    with open("app/model/model_bank_marketing.pkl", "rb") as f:
        model = pickle.load(f)
    return model

scaler = load_scaler()
segment_model = load_segment_model()
final_model = load_final_model()

# -----------------------------
# 2. Función de predicción
# -----------------------------

def predict(input_dict):
    """
    input_dict debe contener las 15 variables originales del dataset:
    age, balance, day, campaign, previous, job, marital, education,
    default, housing, loan, contact, month, poutcome, pdays
    """

    # Convertimos el diccionario en DataFrame
    X = pd.DataFrame([input_dict])

    # -----------------------------
    # Paso 1: Escalar variables numéricas
    # -----------------------------
    numeric_cols = ["age", "balance", "day", "campaign", "previous", "pdays"]

    X_scaled = scaler.transform(X[numeric_cols])
    X[numeric_cols] = X_scaled

    # -----------------------------
    # Paso 2: Generar el segmento
    # -----------------------------
    segment = segment_model.predict(X)[0]
    X["segment"] = segment

    # -----------------------------
    # Paso 3: Predicción final
    # -----------------------------
    final_prediction = final_model.predict(X)[0]

    return {
        "segment": int(segment),
        "prediction": final_prediction
    }
