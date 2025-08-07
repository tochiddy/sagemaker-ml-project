# scripts/upload_to_s3.py

import boto3
import os

s3 = boto3.client("s3")
BUCKET = os.environ.get("SAGEMAKER_BUCKET", "churn-pipeline-sagemaker")

def upload_file(local_path, s3_key):
    s3.upload_file(local_path, BUCKET, s3_key)
    print(f"✅ Uploaded {local_path} → s3://{BUCKET}/{s3_key}")

if __name__ == "__main__":
    upload_file("data/WA_Fn-UseC_-Telco-Customer-Churn.csv", "data/raw.csv")
    upload_file("data/processed/train.csv", "data/train.csv")
    upload_file("data/processed/test.csv", "data/test.csv")
