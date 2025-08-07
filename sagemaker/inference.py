# sagemaker/inference.py

import joblib
import pandas as pd
import os

# Support both SageMaker and local
MODEL_PATH = os.environ.get("MODEL_PATH", "/opt/ml/model/model.joblib")

model = joblib.load(MODEL_PATH)

def predict_fn(input_data, model):
    if isinstance(input_data, pd.DataFrame):
        df = input_data
    else:
        df = pd.DataFrame(input_data)
    
    predictions = model.predict(df)
    return predictions.tolist()
