output "aws_role_to_assume" {
  description = "IAM Role ARN for GitHub Actions (use as AWS_ROLE_TO_ASSUME)"
  value       = aws_iam_role.github_actions.arn
}

output "tf_state_bucket" {
  value = aws_s3_bucket.tf_state.bucket
}

output "tf_lock_table" {
  value = aws_dynamodb_table.tf_locks.name
}
