# Makefile

# Variables
PROJECT_ID = data-eng-bootcamp-project
COOPER_HEVIT_BUCKET_NAME = cooper_hevit_objects
TATE_BUCKET_NAME = tate_objects
MIA_BUCKET_NAME = mia_objects
SPARK_TEMP = spark_temp
TERRAFORM_EXECUTABLE = /home/daniel/Documents/terraform
TERRAFORM_VAR_FILE_INIT = ./vars/init.tfvars
TERRAFORM_VAR_FILE_BQ = ./vars/bq.tfvars

# Targets
init:
	cd ./terraform && $(TERRAFORM_EXECUTABLE) init

apply-init: init
	cd ./terraform && $(TERRAFORM_EXECUTABLE) apply -var-file=$(TERRAFORM_VAR_FILE_INIT)

upload-cooper-hevit:
	python3 ./util/upload_json.py $(PROJECT_ID) $(COOPER_HEVIT_BUCKET_NAME) ./test_data/cooper_hevit/one_line

upload-tate:
	python3 ./util/upload_json.py $(PROJECT_ID) $(TATE_BUCKET_NAME) ./test_data/tate/one_line

upload-mia:
	python3 ./util/upload_json.py $(PROJECT_ID) $(MIA_BUCKET_NAME) ./test_data/mia/one_line

apply-bq: init
	cd ./terraform && $(TERRAFORM_EXECUTABLE) apply -var-file=$(TERRAFORM_VAR_FILE_BQ)

run-spark-cooper-hevit:
	./run_spark.sh cooper_hevit_summary_transform.py google-region $(SPARK_TEMP)

run-spark-mia:
	./run_spark.sh mia_summary_transform.py region $(SPARK_TEMP)

run-spark-tate:
	./run_spark.sh tate_summary_transform.py region $(SPARK_TEMP)

# Default target
all: init apply-init upload-cooper-hevit upload-tate upload-mia apply-bq run-spark-cooper-hevit run-spark-mia run-spark-tate

