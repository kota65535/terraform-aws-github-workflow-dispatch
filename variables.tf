variable "lambda_name" {
  description = "Lambda name"
  type        = string
  default     = "github-workflow-dispatch"
}

variable "lambda_iam_role_name" {
  description = "Lambda IAM role name"
  type        = string
  default     = "github-workflow-dispatch"
}

variable "github_token" {
  description = "GitHub token"
  type        = string
}
