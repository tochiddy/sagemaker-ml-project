output "sagemaker_bucket_name" {
  value = aws_s3_bucket.sagemaker_bucket.bucket
}

output "sagemaker_execution_role_arn" {
  value = aws_iam_role.sagemaker_execution_role.arn
}
