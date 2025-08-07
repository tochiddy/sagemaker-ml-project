terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"      # ← Replace with your bucket name
    key            = "mwaa/sagemaker/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"                  # ← Optional locking table
  }
}
