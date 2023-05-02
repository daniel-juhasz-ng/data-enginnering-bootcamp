# Variables
PROJECT_ID = crime-data-project-385516
PROJECT_REGION = europe-west1
# Make sure this does not change between executions, because it will mess up Terraform
PROJECT_BACKEND_BUCKET_NAME = crime-data-project-tf-state
# Make sure this does not change between executions, because it will mess up Terraform
CRIME_BUCKET_NAME = crime-bucket-unique-name
TERRAFORM_EXECUTABLE = /home/daniel/Documents/terraform

# Targets
create-tf-be:
	gcloud storage buckets create gs://${PROJECT_BACKEND_BUCKET_NAME} --project ${PROJECT_ID} --location ${PROJECT_REGION}

init:
	cd ./terraform && $(TERRAFORM_EXECUTABLE) init -backend-config="bucket=${PROJECT_BACKEND_BUCKET_NAME}"

apply-init: init
	cd ./terraform && $(TERRAFORM_EXECUTABLE) apply \
  -var "project=$(PROJECT_ID)" \
  -var "transform_bigquery=false" \
  -var "load_bigquery=false" \
  -var "region=${PROJECT_REGION}" \
  -var "crime_bucket_name=${CRIME_BUCKET_NAME}" \
  -auto-approve

upload-data:
	python3 ./util/upload_csv.py $(PROJECT_ID) $(CRIME_BUCKET_NAME) ./crime_data

apply-load: init
	cd ./terraform && $(TERRAFORM_EXECUTABLE) apply \
  -var "project=$(PROJECT_ID)" \
  -var "transform_bigquery=false" \
  -var "load_bigquery=true" \
  -var "region=${PROJECT_REGION}" \
  -var "crime_bucket_name=${CRIME_BUCKET_NAME}" \
  -auto-approve

apply-transform: init
	cd ./terraform && $(TERRAFORM_EXECUTABLE) apply \
  -var "project=$(PROJECT_ID)" \
  -var "transform_bigquery=true" \
  -var "load_bigquery=false" \
  -var "region=${PROJECT_REGION}" \
  -var "crime_bucket_name=${CRIME_BUCKET_NAME}" \
  -auto-approve

# Default target
all: create-tf-be init apply-init upload-data apply-load apply-transform

