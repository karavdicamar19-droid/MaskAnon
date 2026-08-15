import argparse
import sys
from pathlib import Path

from maskanon.config import DEFAULT_DATASET_PATH, DEFAULT_MODEL_PATH
from maskanon.predict import predict_batch, predict_single
from maskanon.train import run_training


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maskanon",
        description="Defensive phishing detection CLI (educational and ethical use only).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Train and persist phishing model.")
    train_parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    train_parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    train_parser.add_argument("--test-size", type=float, default=0.2)
    train_parser.add_argument("--random-state", type=int, default=42)

    predict_parser = subparsers.add_parser("predict", help="Classify a single message.")
    predict_parser.add_argument("--text", required=True)
    predict_parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)

    batch_parser = subparsers.add_parser("predict-batch", help="Classify messages from file (.txt or .csv).")
    batch_parser.add_argument("--input", required=True, type=Path)
    batch_parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    batch_parser.add_argument("--output", type=Path)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "train":
            metrics = run_training(
                dataset_path=args.dataset,
                model_path=args.model_path,
                test_size=args.test_size,
                random_state=args.random_state,
            )
            print(f"Model trained and saved to: {args.model_path}")
            print("Validation metrics:")
            for k, v in metrics.items():
                print(f"  - {k}: {v:.4f}")
            return 0

        if args.command == "predict":
            label, confidence = predict_single(text=args.text, model_path=args.model_path)
            print(f"Prediction: {label}")
            if confidence is not None:
                print(f"Confidence: {confidence:.4f}")
            return 0

        if args.command == "predict-batch":
            df = predict_batch(input_path=args.input, model_path=args.model_path, output_path=args.output)
            print(df.to_string(index=False))
            if args.output:
                print(f"Saved batch predictions to: {args.output}")
            return 0

        parser.print_help()
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
