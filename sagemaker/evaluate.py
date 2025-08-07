import argparse
import os
import tarfile
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score

def extract_model(tar_path):
    extract_dir = "extracted_model"
    os.makedirs(extract_dir, exist_ok=True)

    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_dir)

    return os.path.join(extract_dir, "model.joblib")

def evaluate_model(model_tar_path, test_path, threshold=0.75):
    model_path = extract_model(model_tar_path)

    df = pd.read_csv(test_path)
    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    model = joblib.load(model_path)
    preds = model.predict(X)

    accuracy = accuracy_score(y, preds)
    print(f"✅ Model Accuracy: {accuracy:.4f}")

    if accuracy < threshold:
        raise Exception(f"❌ Accuracy {accuracy:.4f} below threshold {threshold}")
    
    return accuracy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Path to model.tar.gz")
    parser.add_argument("--test", type=str, required=True, help="Path to test.csv")
    parser.add_argument("--threshold", type=float, default=0.75)
    args = parser.parse_args()

    evaluate_model(args.model, args.test, args.threshold)
