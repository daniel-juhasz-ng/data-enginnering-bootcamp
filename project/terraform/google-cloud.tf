provider "google" {
  project = var.project
  region  = var.region
}

resource "google_bigquery_dataset" "museum_dataset_raw" {
  dataset_id = "museum_objects_raw"
  location   = "US"
}

resource "google_bigquery_dataset" "museum_dataset_processed" {
  dataset_id = "museum_objects_processed"
  location   = "US"
}

# MIA

resource "google_storage_bucket" "mia_bucket" {
  name = "mia_objects"
  location = var.region
}

resource "google_bigquery_table" "mia_table" {
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
  dataset_id = google_bigquery_dataset.museum_dataset_raw.dataset_id
  table_id = "tate_objects_table"

  external_data_configuration {
    autodetect    = true
    source_format = "NEWLINE_DELIMITED_JSON"
    source_uris   = ["gs://${google_storage_bucket.tate_bucket.name}/*.json"]
  }
}
