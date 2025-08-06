# tests/test_evaluate.py

import os
import subprocess

def test_evaluate_script_runs():
    model_tar = "artifacts/model/model.tar.gz"
    test_data = "data/processed/test.csv"

    assert os.path.exists(model_tar), "Model tar not found"
    assert os.path.exists(test_data), "Test data not found"

    result = subprocess.run([
        "python", "sagemaker/evaluate.py",
        "--model-tar", model_tar,
        "--test-data", test_data,
        "--threshold", "0.5"  # Use a low threshold for test pass
    ], capture_output=True, text=True)

    assert result.returncode == 0, f"Evaluation script failed:\n{result.stderr}"
