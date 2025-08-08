terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    bucket         = "ernike-ml-platform-tfstate"   # <-- your bucket
    key            = "sagemaker-ml-project/infra.tfstate"
    region         = "us-east-1"
    dynamodb_table = "sagemaker-ml-project-locks"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
