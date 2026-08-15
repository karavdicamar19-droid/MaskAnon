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
    model = load_model(model_path)

    @app.route("/", methods=["GET", "POST"])
    def index():
        prediction = None
        confidence = None
        text = ""
        error = None

        if request.method == "POST":
            text = request.form.get("text", "")
            try:
                prediction, confidence = predict_text(model, text)
            except Exception as exc:
                error = str(exc)

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
        text = str(payload.get("text", ""))
        try:
            prediction, confidence = predict_text(model, text)
        except Exception as exc:
            return jsonify({"error": str(exc)}), 400

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
