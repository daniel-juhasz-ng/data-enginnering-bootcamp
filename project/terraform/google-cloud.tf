locals {
  crime_schema = jsondecode(file("./schema/crime_schema.json"))
}

terraform {
  backend "gcs" {
    bucket = "data-eng-bootcamp-tf-state"
    prefix = "terraform/state"
  }
}


provider "google" {
  project = var.project
  region  = var.region
}

resource "google_bigquery_dataset" "crime_raw" {
  dataset_id = "crime_raw"
  location   = var.region
}

resource "google_bigquery_dataset" "crime_processed" {
  dataset_id = "crime_processed"
  location   = var.region
}

resource "google_storage_bucket" "crime_raw_bucket" {
  name     = "crime_raw_bucket"
  location = var.region
}

resource "google_bigquery_table" "crime_table" {
  count = var.create_bigquery ? 1 : 0

  dataset_id = google_bigquery_dataset.crime_raw.dataset_id
  table_id = "crime_table"

  schema = locals.crime_schema

  external_data_configuration {
    autodetect = false
    source_format = "CSV"
    source_uris = ["gs://${google_storage_bucket.crime_raw_bucket.name}/*.csv"]
    csv_options {
      skip_leading_rows = 1
      field_delimiter = ";"
      allow_quoted_newlines = false
      quote = ""
    }
  }
}

# Enable APIs

resource "google_project_service" "bigquery_api" {
  project = var.project
  service = "bigquery.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }

  disable_dependent_services = true
}



