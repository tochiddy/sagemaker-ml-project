terraform {
  backend "local" {} # local backend for one-time bootstrap
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

# -----------------------------
# S3 bucket for Terraform state
# -----------------------------
resource "aws_s3_bucket" "tf_state" {
  bucket = var.tf_state_bucket
}

resource "aws_s3_bucket_versioning" "tf_state" {
  bucket = aws_s3_bucket.tf_state.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tf_state" {
  bucket = aws_s3_bucket.tf_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "tf_state" {
  bucket                  = aws_s3_bucket.tf_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ------------------------------------------
# DynamoDB table for Terraform state locking
# ------------------------------------------
resource "aws_dynamodb_table" "tf_locks" {
  name         = var.tf_lock_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

# ------------------------------------------
# GitHub OIDC provider (create if not exists)
# ------------------------------------------
# These are the current GitHub OIDC root CA thumbprints. Update if GitHub rotates.
# (As of now, GitHub documents 6938fd4d98bab03faadb97b34396831e3780aea1 and 1c58a3a8518e8759bf075b76b750d4f2df264fcd)
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]

  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd"
  ]
}

# ------------------------------------------
# IAM role assumed by GitHub Actions via OIDC
# ------------------------------------------
locals {
  repo_subs = [for b in var.allowed_branches : "repo:${var.github_repo}:ref:${b}"]
  subjects  = concat(local.repo_subs, var.extra_subjects)
}

data "aws_iam_policy_document" "github_assume_role" {
  statement {
    sid     = "AllowGitHubOIDC"
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # Restrict to specific subject(s)
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = local.subjects
    }
  }
}

resource "aws_iam_role" "github_actions" {
  name               = "github-actions-terraform"
  assume_role_policy = data.aws_iam_policy_document.github_assume_role.json
  description        = "Role assumed by GitHub Actions via OIDC to run Terraform"
  max_session_duration = 3600
}

# -------------------------------
# Permissions for the OIDC role
# -------------------------------
# Minimum for remote state + (TEMP) broad perms for your infra apply.
# TODO: tighten to least-privilege policies once infra stabilizes.
resource "aws_iam_role_policy" "terraform_access" {
  role = aws_iam_role.github_actions.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # Remote state S3
      {
        Effect   = "Allow",
        Action   = ["s3:ListBucket"],
        Resource = "arn:aws:s3:::${aws_s3_bucket.tf_state.bucket}"
      },
      {
        Effect   = "Allow",
        Action   = ["s3:GetObject","s3:PutObject","s3:DeleteObject"],
        Resource = "arn:aws:s3:::${aws_s3_bucket.tf_state.bucket}/*"
      },
      # DynamoDB locks
      {
        Effect   = "Allow",
        Action   = ["dynamodb:DescribeTable","dynamodb:GetItem","dynamodb:PutItem","dynamodb:DeleteItem"],
        Resource = "arn:aws:dynamodb:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/${aws_dynamodb_table.tf_locks.name}"
      },
      # TEMP broad permissions for infra (MWAA, SageMaker, IAM, etc.)
      {
        Effect   = "Allow",
        Action   = "*",
        Resource = "*"
      }
    ]
  })
}


#####