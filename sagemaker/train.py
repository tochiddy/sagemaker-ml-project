import argparse
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

def train_model(train_path, model_path):
    df = pd.read_csv(train_path)
    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, f"{model_path}/model.joblib")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=str, required=True)
    parser.add_argument("--model", type=str, required=True)
    args = parser.parse_args()

    train_model(args.train, args.model)
