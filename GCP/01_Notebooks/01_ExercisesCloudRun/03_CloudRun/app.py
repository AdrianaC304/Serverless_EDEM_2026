import os
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Config desde variables de entorno
APP_NAME = os.getenv("APP_NAME", "Flask en Cloud Run")
ENV = os.getenv("ENV", "dev")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "app": APP_NAME,
        "message": "🚀 Hola desde Cloud Run",
        "env": ENV,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route("/echo", methods=["POST"])
def echo():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    return jsonify({
        "you_sent": data,
        "received_at": datetime.utcnow().isoformat() + "Z"
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    }), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    # Cloud Run usa PORT automáticamente
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
