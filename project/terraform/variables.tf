variable "project" {
  type        = string
  description = "The project name"
}

variable "create_bigquery" {
  description = "Whether to create BigQuery tables"
  type        = bool
}

variable "region" {
  description = "Google region name."
  type        = string
  default     = "europe-west1"
}
