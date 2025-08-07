provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "mwaa_dag_bucket" {
  bucket = "churn-pipeline-dags"
  force_destroy = true
}

resource "aws_iam_role" "mwaa_execution_role" {
  name = "MWAAExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "airflow.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "mwaa_policy_attach" {
  role       = aws_iam_role.mwaa_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonMWAAFullAccess"
}

resource "aws_mwaa_environment" "churn_mwaa_env" {
  name                       = "churn-mwaa"
  airflow_version            = "2.9.1"
  dag_s3_path                = "dags"
  source_bucket_arn          = aws_s3_bucket.mwaa_dag_bucket.arn
  execution_role_arn         = aws_iam_role.mwaa_execution_role.arn
  environment_class          = "mw1.small"
  max_workers                = 2
  webserver_access_mode      = "PUBLIC_ONLY"
  requirements_s3_path       = "requirements.txt"
  logging_configuration {
    dag_processing_logs {
      enabled   = true
      log_level = "INFO"
    }
    scheduler_logs {
      enabled   = true
      log_level = "INFO"
    }
    task_logs {
      enabled   = true
      log_level = "INFO"
    }
    webserver_logs {
      enabled   = true
      log_level = "INFO"
    }
    worker_logs {
      enabled   = true
      log_level = "INFO"
    }
  }
  airflow_configuration_options = {
    "core.default_timezone" = "utc"
  }
}
