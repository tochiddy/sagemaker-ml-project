import joblib
import pandas as pd
import os

def model_fn(model_dir=None):
    # Allow override for testing
    if model_dir is None:
        model_dir = os.environ.get("MODEL_PATH", "/opt/ml/model")
    model_path = os.path.join(model_dir, "model.joblib")
    return joblib.load(model_path)

def predict_fn(input_data, model):
    if isinstance(input_data, pd.DataFrame):
        df = input_data
    else:
        df = pd.DataFrame(input_data)
    return model.predict(df).tolist()
