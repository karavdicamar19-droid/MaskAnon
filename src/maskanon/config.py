from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_PATH = ROOT_DIR / "data" / "sample_phishing_messages.csv"
DEFAULT_ARTIFACT_DIR = ROOT_DIR / "artifacts"
DEFAULT_MODEL_PATH = DEFAULT_ARTIFACT_DIR / "phishing_model.joblib"
