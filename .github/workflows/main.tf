terraform {
  backend "s3" {
    bucket = "terraform-backend-561678142736"
    region = "ap-northeast-1"
    key    = "terraform-aws-github-workflow-dispatch.tfstate"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.52.0"
    }
  }
  required_version = "~> 1.8.0"
}

provider "aws" {
  region = "ap-northeast-1"
}

module "workflow_dispatch" {
  source = "../../"

  github_token = var.github_token
}
