from pathlib import Path

import pandas as pd

from maskanon.model import load_model, predict_text


def predict_single(text: str, model_path: Path) -> tuple[str, float | None]:
    model = load_model(model_path)
    return predict_text(model, text)


def predict_batch(input_path: Path, model_path: Path, output_path: Path | None = None) -> pd.DataFrame:
    model = load_model(model_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix.lower() == ".csv":
        df = pd.read_csv(input_path)
        if "text" not in df.columns:
            raise ValueError("CSV batch file must contain a 'text' column.")
        texts = df["text"].astype(str).tolist()
        result_df = df.copy()
    else:
        texts = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        result_df = pd.DataFrame({"text": texts})

    if not texts:
        raise ValueError("No input messages found for batch prediction.")

    labels: list[str] = []
    confidences: list[float | None] = []

    for text in texts:
        label, confidence = predict_text(model, text)
        labels.append(label)
        confidences.append(confidence)

    result_df["prediction"] = labels
    result_df["confidence"] = confidences

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result_df.to_csv(output_path, index=False)

    return result_df
