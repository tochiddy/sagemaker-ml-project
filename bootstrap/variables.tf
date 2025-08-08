variable "aws_region" {
  description = "AWS region for all bootstrap resources"
  type        = string
}

variable "tf_state_bucket" {
  description = "Globally-unique S3 bucket name for Terraform remote state"
  type        = string
}

variable "tf_lock_table" {
  description = "DynamoDB table name for Terraform state locks"
  type        = string
  default     = "sagemaker-ml-project-locks"
}

variable "github_repo" {
  description = "GitHub repo in 'owner/name' format (e.g., my-org/sagemaker-ml-project)"
  type        = string
}

# Optional: restrict which branches can assume the role
variable "allowed_branches" {
  description = "List of branch refs allowed to assume the role"
  type        = list(string)
  default     = ["refs/heads/main"]
}

# Optional: broader subject claims (e.g., environments). Leave empty unless needed.
variable "extra_subjects" {
  description = "Additional exact sub claims allowed (e.g., repo:org/repo:environment:prod)"
  type        = list(string)
  default     = []
}
