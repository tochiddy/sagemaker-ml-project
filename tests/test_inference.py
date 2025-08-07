import os
import pytest
from sagemaker.inference import model_fn, predict_fn

def test_predict_fn_with_real_model():
    model_path = "artifacts/model"
    assert os.path.exists(os.path.join(model_path, "model.joblib")), "Trained model not found."

    model = model_fn(model_path)

    input_data = [{
        "gender": 1,
        "SeniorCitizen": 0,
        "Partner": 1,
        "Dependents": 0,
        "tenure": 5,
        "PhoneService": 1,
        "MultipleLines": 0,
        "InternetService": 2,
        "OnlineSecurity": 0,
        "OnlineBackup": 1,
        "DeviceProtection": 0,
        "TechSupport": 0,
        "StreamingTV": 1,
        "StreamingMovies": 0,
        "Contract": 0,
        "PaperlessBilling": 1,
        "PaymentMethod": 2,
        "MonthlyCharges": 70.35,
        "TotalCharges": 350.5
    }]

    predictions = predict_fn(input_data, model)
    assert isinstance(predictions, list)
    assert len(predictions) == 1
    assert predictions[0] in [0, 1]  # Churn prediction should be binary
