from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"text", "label"}
VALID_LABELS = {"phishing", "legitimate"}


def load_dataset(dataset_path: Path) -> pd.DataFrame:
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    df = pd.read_csv(dataset_path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {sorted(missing)}")

    df = df.copy()
    df["text"] = df["text"].astype(str).str.strip()
    df["label"] = df["label"].astype(str).str.strip().str.lower()

    df = df[(df["text"] != "") & (df["label"].isin(VALID_LABELS))]
    if df.empty:
        raise ValueError("Dataset has no valid rows after cleaning.")

    if set(df["label"].unique()) != VALID_LABELS:
        raise ValueError(
            "Dataset must include at least one phishing and one legitimate sample."
        )

    return df
