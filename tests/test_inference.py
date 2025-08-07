# tests/test_inference.py

import pandas as pd
from sagemaker.inference import predict_fn, model

def test_inference_prediction():
    # Use small sample of real data
    df = pd.read_csv("data/processed/test.csv").drop("Churn", axis=1).head(3)
    preds = predict_fn(df, model)
    
    assert isinstance(preds, list), "Predictions should be a list"
    assert len(preds) == len(df), "Mismatch in number of predictions"
    assert all(pred in [0, 1] for pred in preds), "Invalid prediction values"
