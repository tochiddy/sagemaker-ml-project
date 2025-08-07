resource "aws_s3_bucket" "sagemaker_bucket" {
  bucket = "churn-pipeline-sagemaker"
  force_destroy = true
}

resource "aws_iam_role" "sagemaker_execution_role" {
  name = "SageMakerExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "sagemaker.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "sagemaker_policy" {
  name = "SageMakerS3Policy"
  role = aws_iam_role.sagemaker_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:*"
        ],
        Resource = [
          aws_s3_bucket.sagemaker_bucket.arn,
          "${aws_s3_bucket.sagemaker_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "sagemaker:*",
          "cloudwatch:*",
          "logs:*",
          "ecr:GetAuthorizationToken",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ],
        Resource = "*"
      }
    ]
  })
}
