variable "project" {
  type        = string
  description = "The project name"
}

variable "load_bigquery" {
  description = "Whether to load BigQuery data"
  type        = bool
}

variable "transform_bigquery" {
  description = "Whether to transform BigQuery data"
  type        = bool
}

variable "region" {
  description = "Google region name."
  type        = string
}

variable "crime_bucket_name" {
  description = "Name for the bucket, which will store crime raw data."
  type        = string
}
