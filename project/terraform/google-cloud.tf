provider "google" {
  project = var.project
  region  = var.region
}

resource "google_bigquery_dataset" "museum_dataset_raw" {
  dataset_id = "museum_objects_raw"
  location   = var.region
}

resource "google_bigquery_dataset" "museum_dataset_processed" {
  dataset_id = "museum_objects_processed"
  location   = var.region
}

# MIA

resource "google_storage_bucket" "mia_bucket" {
  name = "mia_objects"
  location = var.region
}

resource "google_bigquery_table" "mia_table" {
  count  = var.create_bigquery ? 1 : 0

  dataset_id = google_bigquery_dataset.museum_dataset_raw.dataset_id
  table_id = "mia_objects_table"

  external_data_configuration {
    autodetect    = true
    source_format = "NEWLINE_DELIMITED_JSON"
    source_uris   = ["gs://${google_storage_bucket.mia_bucket.name}/*.json"]
  }
}

# Cooper Hevit

resource "google_storage_bucket" "cooper_hevit_bucket" {
  name = "cooper_hevit_objects"
  location = var.region
}

resource "google_bigquery_table" "cooper_hevit_table" {
  count  = var.create_bigquery ? 1 : 0

  dataset_id = google_bigquery_dataset.museum_dataset_raw.dataset_id
  table_id = "cooper_hevit_objects_table"

  external_data_configuration {
    autodetect    = true
    source_format = "NEWLINE_DELIMITED_JSON"
    source_uris   = ["gs://${google_storage_bucket.cooper_hevit_bucket.name}/*.json"]
  }
}

# Tate

resource "google_storage_bucket" "tate_bucket" {
  name = "tate_objects"
  location = var.region
}

resource "google_bigquery_table" "tate_table" {
  count  = var.create_bigquery ? 1 : 0

  dataset_id = google_bigquery_dataset.museum_dataset_raw.dataset_id
  table_id = "tate_objects_table"

  external_data_configuration {
    autodetect    = true
    source_format = "NEWLINE_DELIMITED_JSON"
    source_uris   = ["gs://${google_storage_bucket.tate_bucket.name}/*.json"]
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


resource "google_project_service" "dataproc_api" {
  project = var.project
  service = "dataproc.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }

  disable_dependent_services = true
}


