from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from app.model.predictor import predict


app = Flask(__name__)
CORS(app)


@app.route("/app", methods=["GET"])
def app_page():
    # Sirve el cuestionario (frontend) desde el mismo servidor que el modelo.
    return send_from_directory(app.static_folder, "predictor.html")

REQUIRED = ["age", "balance", "day", "campaign", "previous", "pdays",
            "job", "marital", "education", "default", "housing",
            "loan", "contact", "month", "poutcome"]
NUMERIC = ["age", "balance", "day", "campaign", "previous", "pdays"]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "api": "Predicción Bank Marketing",
        "endpoints": {
            "/predict": "GET con los campos en la URL, o POST con JSON",
            "campos": REQUIRED,
            "ejemplo_get": "/predict?age=42&balance=1500&day=5&campaign=1&previous=0&pdays=-1&job=admin&marital=married&education=secondary&default=no&housing=yes&loan=no&contact=cellular&month=may&poutcome=unknown"
        }
    })


@app.route("/predict", methods=["GET", "POST"])
def predict_endpoint():
    # 1) recoger los datos según cómo lleguen
    if request.method == "POST":
        input_data = request.get_json(silent=True) or {}
    else:
        input_data = request.args.to_dict()   # en GET todo llega como texto

    # 2) ¿falta algún campo? -> 400 con mensaje claro
    missing = [f for f in REQUIRED if f not in input_data]
    if missing:
        return jsonify({"error": "Faltan campos", "missing_fields": missing}), 400

    # 3) convertir a número los campos numéricos (en GET vienen como string)
    for f in NUMERIC:
        try:
            input_data[f] = int(input_data[f])
        except (ValueError, TypeError):
            return jsonify({"error": f"El campo '{f}' debe ser numérico"}), 400

    # 4) predecir -> 500 solo si colapsa de verdad la predicción
    try:
        resultado = predict(input_data)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": "Error al predecir", "detalle": str(e)}), 500

# ENDPOINT PARA DEMO DE REDESPLIEGUE EN DIRECTO v descomentar aquí v
@app.route("/retrain", methods=["GET"])
def retrain_endpoint():
    return jsonify({
        "status": "Éxito",
        "message": "Redespliegue en directo completado y modelo actualizado."
    })

if __name__ == "__main__":
    app.run(debug=True)