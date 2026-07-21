"""src/api/app.py — Flask REST API for KRA-LIP."""
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.utils.logger import get_logger
from config.settings import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, SECRET_KEY

logger = get_logger(__name__)
app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app)


@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "KRA-LIP API", "version": "1.0"}), 200


@app.route("/predict/case", methods=["POST"])
def predict_case():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No JSON body provided"}), 400
        from src.case_predictor.predictor import predict_case as _predict
        result = _predict(data)
        return jsonify({"status": "success", "data": result}), 200
    except FileNotFoundError:
        return jsonify({"error": "Model not found. Run trainer first."}), 503
    except Exception as e:
        logger.error("Prediction error: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/classify/document", methods=["POST"])
def classify_document():
    try:
        data = request.get_json(force=True)
        if not data or "text" not in data:
            return jsonify({"error": "Provide { 'text': '<document text>' }"}), 400
        from src.document_intelligence.classifier import classify_document as _classify
        result = _classify(data["text"])
        return jsonify({"status": "success", "data": result}), 200
    except FileNotFoundError:
        return jsonify({"error": "Document model not found. Run trainer first."}), 503
    except Exception as e:
        logger.error("Classification error: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/predict/case/batch", methods=["POST"])
def predict_batch():
    try:
        data = request.get_json(force=True)
        cases = data.get("cases", [])
        if not cases:
            return jsonify({"error": "Provide { 'cases': [ ... ] }"}), 400
        from src.case_predictor.predictor import predict_batch as _batch
        results = _batch(cases)
        return jsonify({"status": "success", "count": len(results), "data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.info("Starting KRA-LIP API on %s:%s", FLASK_HOST, FLASK_PORT)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
