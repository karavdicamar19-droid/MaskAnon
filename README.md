# MaskAnon (Defensive Phishing Detection AI)

> **Legal & Ethical Notice:** This project is strictly for defensive cybersecurity, education, and awareness.
> It must **not** be used for phishing, credential theft, malware delivery, exploit development, or any unauthorized activity.

MaskAnon is a complete Python application for classifying message text as `phishing` or `legitimate` using a standard ML pipeline (TF-IDF + Logistic Regression).

## Project structure

- `src/maskanon/` — package source code
  - `train.py` — model training orchestration
  - `predict.py` — single and batch inference helpers
  - `cli.py` — command-line interface
  - `webapp.py` — Flask web UI + JSON API
- `data/sample_phishing_messages.csv` — safe sample dataset
- `artifacts/` — persisted model artifacts (generated locally)
- `requirements.txt` — runtime dependencies
- `pyproject.toml` — package setup

## Setup

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Train model

```bash
python -m maskanon.cli train \
  --dataset data/sample_phishing_messages.csv \
  --model-path artifacts/phishing_model.joblib
```

## Predict single message (CLI)

```bash
python -m maskanon.cli predict \
  --text "Urgent: verify your account now at https://example-login-check.test" \
  --model-path artifacts/phishing_model.joblib
```

## Batch scoring (CLI, optional)

Input can be `.txt` (one message per line) or `.csv` (must include `text` column).

```bash
python -m maskanon.cli predict-batch \
  --input data/sample_phishing_messages.csv \
  --model-path artifacts/phishing_model.joblib \
  --output artifacts/batch_predictions.csv
```

## Run Flask web app

```bash
python -m maskanon.webapp
```

Then open `http://127.0.0.1:5000`.

### JSON API example

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Please verify your account password immediately."}'
```

## Replacing sample dataset with real data

Use a CSV with columns:

- `text` — raw message text
- `label` — `phishing` or `legitimate`

Keep class labels normalized to those exact values. Then pass your dataset path via `--dataset` during training.

## Troubleshooting

- **`Model not found ... Run training first`**
  - Train first with `python -m maskanon.cli train ...`.
- **`Dataset missing required columns`**
  - Ensure CSV has `text,label` header.
- **Import/module errors for `maskanon`**
  - Re-run `pip install -e .` from repo root.
- **Flask app fails at startup due to missing model**
  - Generate `artifacts/phishing_model.joblib` by running the train command.

## Defensive-use disclaimer

This repository intentionally excludes offensive capabilities and abuse-oriented instructions.
It is designed only to help users detect and reduce phishing risk in legal, authorized contexts.
