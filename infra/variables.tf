variable "region" {
  default = "us-east-1"
}

variable "sagemaker_bucket_name" {
  default = "churn-pipeline-sagemaker"
}

variable "dag_bucket_name" {
  default = "churn-pipeline-dags"
}

variable "mwaa_env_name" {
  default = "churn-mwaa"
}

variable "execution_role_name" {
  default = "SageMakerExecutionRole"
}
