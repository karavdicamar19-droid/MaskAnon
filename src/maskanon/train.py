from pathlib import Path

from maskanon.data import load_dataset
from maskanon.model import save_model, train_model


def run_training(dataset_path: Path, model_path: Path, test_size: float, random_state: int) -> dict[str, float]:
    df = load_dataset(dataset_path)
    model, metrics = train_model(df, test_size=test_size, random_state=random_state)
    save_model(model, model_path)
    return metrics
