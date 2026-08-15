from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


ModelBundle = dict[str, Any]


def build_pipeline(random_state: int = 42) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=1,
                    max_features=5000,
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000, random_state=random_state)),
        ]
    )


def train_model(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> tuple[Pipeline, dict[str, float]]:
    x_train, x_valid, y_train, y_valid = train_test_split(
        df["text"],
        df["label"],
        test_size=test_size,
        random_state=random_state,
        stratify=df["label"],
    )

    model = build_pipeline(random_state=random_state)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_valid)
    metrics = {
        "accuracy": float(accuracy_score(y_valid, y_pred)),
        "precision": float(precision_score(y_valid, y_pred, pos_label="phishing")),
        "recall": float(recall_score(y_valid, y_pred, pos_label="phishing")),
        "f1": float(f1_score(y_valid, y_pred, pos_label="phishing")),
    }

    return model, metrics


def save_model(model: Pipeline, model_path: Path) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    bundle: ModelBundle = {"model": model}
    joblib.dump(bundle, model_path)


def load_model(model_path: Path) -> Pipeline:
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run training first with `python -m maskanon.cli train`."
        )

    bundle = joblib.load(model_path)
    model = bundle.get("model")
    if model is None:
        raise ValueError(f"Invalid model artifact at {model_path}.")
    return model


def predict_text(model: Pipeline, text: str) -> tuple[str, float | None]:
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Input text is empty.")

    pred = str(model.predict([cleaned])[0])
    confidence: float | None = None

    if hasattr(model[-1], "predict_proba"):
        proba = model.predict_proba([cleaned])[0]
        confidence = float(max(proba))

    return pred, confidence
