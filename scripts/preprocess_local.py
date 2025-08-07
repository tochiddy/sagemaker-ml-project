# scripts/preprocess_local.py

import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def preprocess(input_path: str, output_dir: str):
    print(f"📥 Reading data from: {input_path}")
    df = pd.read_csv(input_path)

    # Drop customerID
    if "customerID" in df.columns:
        df.drop("customerID", axis=1, inplace=True)

    # Convert TotalCharges to numeric
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)

    # Encode target
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # Encode categorical columns
    cat_cols = df.select_dtypes(include=["object"]).columns
    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col])

    # Train/test split
    train, test = train_test_split(df, test_size=0.2, random_state=42, stratify=df["Churn"])

    # Ensure output dir exists
    os.makedirs(output_dir, exist_ok=True)

    # Save
    train_path = os.path.join(output_dir, "train.csv")
    test_path = os.path.join(output_dir, "test.csv")
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)

    print(f"✅ Preprocessing complete. Train and test saved to {output_dir}/")
    print(f"🔢 Train shape: {train.shape} | Test shape: {test.shape}")
    print(f"🎯 Churn distribution in train: {train['Churn'].value_counts(normalize=True).to_dict()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local preprocessing for Telco churn dataset.")
    parser.add_argument("--input", type=str, default="data/telco_churn_raw.csv", help="Path to raw input CSV.")
    parser.add_argument("--output", type=str, default="data/processed", help="Directory to save processed files.")
    args = parser.parse_args()

    preprocess(args.input, args.output)
