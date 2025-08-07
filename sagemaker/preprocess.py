import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def preprocess(input_path: str, output_dir: str):
    df = pd.read_csv(input_path)

    # Drop customerID (irrelevant)
    df.drop('customerID', axis=1, inplace=True)

    # Convert total charges to numeric (some are empty strings)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)

    # Binary encode target column
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

    # Label encode all categorical columns
    cat_cols = df.select_dtypes(include=['object']).columns
    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col])

    # Train/test split
    train, test = train_test_split(df, test_size=0.2, random_state=42)

    # Output CSVs
    train.to_csv(f"{output_dir}/train.csv", index=False)
    test.to_csv(f"{output_dir}/test.csv", index=False)

    print("Preprocessing complete. Train/test sets saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/telco_churn_raw.csv")
    parser.add_argument("--output", type=str, default="data/processed")
    args = parser.parse_args()

    preprocess(args.input, args.output)
