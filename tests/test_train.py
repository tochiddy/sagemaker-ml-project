# tests/test_train.py

import os
import pandas as pd
from sagemaker.train import train_model

def test_train_script_runs():
    os.makedirs("data/test_model", exist_ok=True)
    train_model("data/processed/train.csv", "data/test_model")
    assert os.path.exists("data/test_model/model.joblib")
