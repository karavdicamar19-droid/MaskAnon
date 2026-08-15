from pathlib import Path

from flask import Flask, jsonify, render_template_string, request

from maskanon.config import DEFAULT_MODEL_PATH
from maskanon.model import load_model, predict_text

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>MaskAnon Defensive Phishing Detection</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 820px; margin: 2rem auto; padding: 0 1rem; }
      textarea { width: 100%; min-height: 120px; }
      .card { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-top: 1rem; }
      .warn { color: #8b0000; font-weight: bold; }
    </style>
  </head>
  <body>
    <h1>MaskAnon Defensive Phishing Detection</h1>
    <p class="warn">For legal, ethical, defensive use only.</p>
    <form method="post">
      <label for="text">Message text</label><br>
      <textarea id="text" name="text" required>{{ (text or "") | e }}</textarea><br><br>
      <button type="submit">Classify</button>
    </form>

    {% if error %}
      <p class="warn">{{ error }}</p>
    {% endif %}

    {% if prediction %}
      <div class="card">
        <h2>Result</h2>
        <p><strong>Prediction:</strong> {{ prediction }}</p>
        {% if confidence is not none %}
          <p><strong>Confidence:</strong> {{ "%.2f"|format(confidence * 100) }}%</p>
        {% endif %}
      </div>
    {% endif %}
  </body>
</html>
"""


def create_app(model_path: Path = DEFAULT_MODEL_PATH) -> Flask:
    app = Flask(__name__)
    model = None
    startup_error = None

    try:
        model = load_model(model_path)
    except FileNotFoundError:
        startup_error = (
            f"Model not found at {model_path}. Train first with "
            "`python -m maskanon.cli train --dataset data/sample_phishing_messages.csv --model-path artifacts/phishing_model.joblib`."
        )

    @app.route("/", methods=["GET", "POST"])
    def index():
        prediction = None
        confidence = None
        text = ""
        error = startup_error

        if request.method == "POST":
            text = request.form.get("text", "")
            if model is None:
                error = startup_error
            else:
                try:
                    prediction, confidence = predict_text(model, text)
                except ValueError as exc:
                    error = str(exc)
                except Exception:
                    error = "Prediction failed due to an internal server error."

        return render_template_string(
            HTML_TEMPLATE,
            prediction=prediction,
            confidence=confidence,
            text=text,
            error=error,
        )

    @app.route("/api/predict", methods=["POST"])
    def api_predict():
        payload = request.get_json(silent=True) or {}
        if "text" not in payload:
            return jsonify({"error": "Missing required field: text"}), 400

        raw_text = payload["text"]
        if not isinstance(raw_text, str):
            return jsonify({"error": "Field 'text' must be a string."}), 400

        text = raw_text
        if not text.strip():
            return jsonify({"error": "Field 'text' must be a non-empty string."}), 400

        if model is None:
            return jsonify({"error": startup_error}), 503

        try:
            prediction, confidence = predict_text(model, text)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception:
            return jsonify({"error": "Prediction failed due to an internal server error."}), 500

        return jsonify(
            {
                "prediction": prediction,
                "confidence": confidence,
                "disclaimer": "Defensive phishing detection only. Do not use for abuse.",
            }
        )

    return app


def main() -> None:
    app = create_app(DEFAULT_MODEL_PATH)
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
