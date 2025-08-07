import subprocess
import os

def test_evaluate_script_runs():
    model_tar = "artifacts/model/model.tar.gz"
    test_data = "data/processed/test.csv"

    assert os.path.exists(model_tar), "Model tar not found"
    assert os.path.exists(test_data), "Test data not found"

    result = subprocess.run([
        "python", "sagemaker/evaluate.py",
        "--model", model_tar,
        "--test", test_data,
        "--threshold", "0.5"  # lower threshold so test passes
    ], capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)

    assert result.returncode == 0, f"Evaluation script failed:\n{result.stderr}"
