variable "project" {
  type        = string
  description = "The project name"
}

variable "environment" {
  description = "Environment name, e.g. `staging`, `production`."
  type        = string
}

variable "region" {
  description = "AWS region name."
  type        = string
  default     = "us-central1"
}
