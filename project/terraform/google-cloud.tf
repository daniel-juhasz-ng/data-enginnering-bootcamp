locals {
  crime_schema           = jsondecode(file("./schema/crime_schema.json"))
  crime_processed_schema = jsondecode(file("./schema/crime_processed_schema.json"))
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

resource "google_bigquery_table" "crime_raw_table" {
  deletion_protection = false

  schema = jsonencode(local.crime_schema)

  dataset_id = google_bigquery_dataset.crime_raw.dataset_id
  table_id   = "crime_raw_table"
}

resource "google_bigquery_table" "crime_processed_table" {
  deletion_protection = false

  schema = jsonencode(local.crime_processed_schema)

  range_partitioning {
    field = "year"
    range {
      start    = 2020
      end      = 2030
      interval = 1
    }
  }

  clustering = ["month"]

  dataset_id = google_bigquery_dataset.crime_processed.dataset_id
  table_id   = "crime_processed_table"
}


resource "google_bigquery_job" "load_crime_job" {
  count    = var.create_bigquery ? 1 : 0
  job_id   = "load_crime_data_to_bq_2"
  location = var.region

  load {
    source_uris = [
      "gs://${google_storage_bucket.crime_raw_bucket.name}/*.csv"
    ]

    destination_table {
      table_id = "projects/${google_bigquery_table.crime_raw_table.project}/datasets/${google_bigquery_table.crime_raw_table.dataset_id}/tables/${google_bigquery_table.crime_raw_table.table_id}"
    }

    skip_leading_rows     = 1
    schema_update_options = ["ALLOW_FIELD_RELAXATION", "ALLOW_FIELD_ADDITION"]

    write_disposition = "WRITE_APPEND"
    autodetect        = true
  }
}

resource "google_bigquery_job" "transform_crime_job" {
  count    = var.transform_bigquery ? 1 : 0
  job_id   = "transform_crime_data"
  location = var.region

  query {
    query = "SELECT SPLIT(month, '-')[SAFE_OFFSET(0)] AS year, SPLIT(month, '-')[SAFE_OFFSET(1)] AS month, reported_by, crime_type FROM ${google_bigquery_table.crime_raw_table.project}:${google_bigquery_table.crime_raw_table.dataset_id}.${google_bigquery_table.crime_raw_table.table_id}"

    destination_table {
      table_id = google_bigquery_table.crime_processed_table.table_id
    }

    default_dataset {
      dataset_id = google_bigquery_dataset.crime_raw.id
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



