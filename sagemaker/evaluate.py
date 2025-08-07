import argparse
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score

def evaluate_model(model_path, test_path):
    df = pd.read_csv(test_path)
    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    model = joblib.load(model_path)
    preds = model.predict(X)

    accuracy = accuracy_score(y, preds)
    print(f"Model Accuracy: {accuracy}")
    return accuracy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--test", type=str, required=True)
    args = parser.parse_args()

    acc = evaluate_model(args.model, args.test)
    if acc < 0.75:
        raise Exception("Accuracy below threshold.")
