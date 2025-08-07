#!/bin/bash

echo "🧪 Running all tests..."

# Ensure test folders exist
mkdir -p artifacts/model

# Run preprocessing
echo "📦 Running preprocessing..."
python scripts/preprocess_local.py

# Run training
echo "🧠 Training model..."
python sagemaker/train.py --train data/processed/train.csv --model artifacts/model

# Package model
echo "📦 Compressing model..."
tar -czf artifacts/model/model.tar.gz -C artifacts/model model.joblib

# Run evaluation test
echo "✅ Testing evaluation script..."
pytest tests/test_evaluate.py

# Run DAG test
echo "📊 Testing DAG loading..."
pytest tests/test_dag.py

echo "🎉 All tests completed successfully!"
