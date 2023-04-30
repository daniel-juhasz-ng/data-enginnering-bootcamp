# Makefile

# Variables
PROJECT_ID = data-eng-bootcamp-project
CRIME_RAW_BUCKET_NAME = crime_raw_bucket
TERRAFORM_EXECUTABLE = /home/daniel/Documents/terraform
TERRAFORM_VAR_FILE_INIT = ./vars/init.tfvars
TERRAFORM_VAR_FILE_BQ = ./vars/bq.tfvars
TERRAFORM_VAR_FILE_TRANSFORM = ./vars/transform.tfvars

# Targets
init:
	cd ./terraform && $(TERRAFORM_EXECUTABLE) init

apply-init: init
	cd ./terraform && $(TERRAFORM_EXECUTABLE) apply -var-file=$(TERRAFORM_VAR_FILE_INIT)

upload-data:
	python3 ./util/upload_csv.py $(PROJECT_ID) $(CRIME_RAW_BUCKET_NAME) ./crime_data

apply-bq: init
	cd ./terraform && $(TERRAFORM_EXECUTABLE) apply -var-file=$(TERRAFORM_VAR_FILE_BQ)

apply-transform: init
	cd ./terraform && $(TERRAFORM_EXECUTABLE) apply -var-file=$(TERRAFORM_VAR_FILE_TRANSFORM)

# Default target
all: init apply-init upload-data apply-bq apply-transform

