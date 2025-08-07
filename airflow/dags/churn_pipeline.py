from airflow import DAG
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
from airflow.providers.amazon.aws.operators.sagemaker import (
    SageMakerTrainingOperator,
    SageMakerModelOperator,
    SageMakerEndpointConfigOperator,
    SageMakerEndpointOperator,
)
from airflow.utils.dates import days_ago
import os

BUCKET = os.getenv("SAGEMAKER_BUCKET", "churn-pipeline-sagemaker")
ROLE_ARN = os.getenv("SAGEMAKER_ROLE_ARN", "<your-role-arn>")
MODEL_NAME = "churn-model"
ENDPOINT_NAME = "churn-endpoint"

TRAINING_JOB_NAME = "churn-training-job"
IMAGE_URI = "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.5-1"  # Example

default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG("churn_sagemaker_pipeline",
         default_args=default_args,
         start_date=days_ago(1),
         schedule_interval="@weekly",
         catchup=False) as dag:

    # Upload training data (you can use a ProcessingJob instead)
    upload_train_data = S3CreateObjectOperator(
        task_id="upload_train_data",
        s3_bucket=BUCKET,
        s3_key="data/train.csv",
        data="{{ var.value.train_data }}",  # load from variable
        replace=True,
    )

    # Launch SageMaker training job
    train_model = SageMakerTrainingOperator(
        task_id="train_model",
        config={
            "TrainingJobName": TRAINING_JOB_NAME,
            "AlgorithmSpecification": {
                "TrainingImage": IMAGE_URI,
                "TrainingInputMode": "File"
            },
            "RoleArn": ROLE_ARN,
            "InputDataConfig": [{
                "ChannelName": "train",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": f"s3://{BUCKET}/data/",
                        "S3DataDistributionType": "FullyReplicated",
                    }
                },
                "ContentType": "text/csv"
            }],
            "OutputDataConfig": {
                "S3OutputPath": f"s3://{BUCKET}/output/"
            },
            "ResourceConfig": {
                "InstanceType": "ml.m5.large",
                "InstanceCount": 1,
                "VolumeSizeInGB": 5
            },
            "StoppingCondition": {
                "MaxRuntimeInSeconds": 600
            }
        },
    )

    create_model = SageMakerModelOperator(
        task_id="create_model",
        config={
            "ModelName": MODEL_NAME,
            "PrimaryContainer": {
                "Image": IMAGE_URI,
                "ModelDataUrl": f"s3://{BUCKET}/output/{TRAINING_JOB_NAME}/output/model.tar.gz"
            },
            "ExecutionRoleArn": ROLE_ARN
        }
    )

    create_endpoint_config = SageMakerEndpointConfigOperator(
        task_id="create_endpoint_config",
        config={
            "EndpointConfigName": f"{ENDPOINT_NAME}-config",
            "ProductionVariants": [{
                "VariantName": "AllTraffic",
                "ModelName": MODEL_NAME,
                "InitialInstanceCount": 1,
                "InstanceType": "ml.m5.large"
            }]
        }
    )

    deploy_endpoint = SageMakerEndpointOperator(
        task_id="deploy_endpoint",
        config={
            "EndpointName": ENDPOINT_NAME,
            "EndpointConfigName": f"{ENDPOINT_NAME}-config"
        }
    )

    upload_train_data >> train_model >> create_model >> create_endpoint_config >> deploy_endpoint
