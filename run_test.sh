#!/bin/bash

set -e  # Exit on any error

echo "🔁 Starting local MLOps test pipeline..."

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ venv not found. Please create it using: python3 -m venv venv"
    exit 1
fi

# Preprocess data
echo "📊 Preprocessing data..."
python scripts/preprocess_local.py

# Train model
echo "🧠 Training model..."
python sagemaker/train.py --train data/processed/train.csv --model artifacts/model

# Package model
echo "📦 Packaging model to model.tar.gz..."
tar -czf artifacts/model/model.tar.gz -C artifacts/model model.joblib

# Evaluate model
echo "✅ Evaluating model..."
python sagemaker/evaluate.py --model artifacts/model/model.tar.gz --test data/processed/test.csv

# Run unit tests
echo "🧪 Running all tests..."
pytest tests/

echo "🎉 All tests passed successfully!"
