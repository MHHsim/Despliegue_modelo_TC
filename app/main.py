from flask import Flask, request, jsonify
from app.model.predictor import predict

app = Flask(_name_)

@app.route("/", methods=["GET"])
def home():
    return "API del modelo Bank Marketing funcionando correctamente"

# -----------------------------
# ENDPOINT DE PREDICCIÓN
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict_endpoint():
    try:
        # Recibir JSON del cliente
        input_data = request.get_json()

        # Validación mínima
        required_fields = [
            "age", "balance", "day", "campaign", "previous",
            "job", "marital", "education", "default", "housing",
            "loan", "contact", "month", "poutcome", "pdays"
        ]

        missing = [field for field in required_fields if field not in input_data]
        if missing:
            return jsonify({
                "error": "Missing fields",
                "missing_fields": missing
            }), 400

        # Llamar a tu predictor
        resultado = predict(input_data)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if _name_ == "_main_":
    app.run(debug=True)