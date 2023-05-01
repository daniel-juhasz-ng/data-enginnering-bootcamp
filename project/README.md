## Introduction

The [UK based crimes dataset](https://data.police.uk/) is a valuable resource for researchers, analysts, and policymakers interested in understanding crime patterns and trends in the UK. The dataset provides information about the types of crimes committed, the police forces that respond to the crimes, and the dates of the crimes. This data report aims to provide an analysis of the crimes reported in the dataset, highlighting the frequency of different types of crimes and the workload of each police force in responding to the crimes.

Understanding crime patterns and trends is essential for designing effective policies and interventions to prevent and reduce crime. By analyzing the data in this report, policymakers can identify areas of the UK where specific types of crimes are more prevalent and allocate resources accordingly. Furthermore, law enforcement agencies can use the data to better understand their workload and prioritize resources to ensure the safety of the public.

Overall, this data report provides valuable insights into the UK's crime landscape, which can inform evidence-based policy and decision-making.

## The project


![alt text](architecture.png "Architecture")

The project utilizes Google Cloud and its offered features, including:

- **Cloud Storage**: For storing initial data
- **BigQuery**: Data warehouse solution, which helps processing and storing the data for the later stages in an optimized way
- **Data Studio**: Although not necessarily part of Google Cloud, but it is a Google product. It serves as the visualization solution for the data

## How to


Make sure that python is installed (Terraform scripts run with auto approve!)

1. Create project by hand
2. Make sure billing is enabled
3. Install gcloud and
   authenticate https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/provider_reference#running-terraform-on-your-workstation
   so you can run the Terraform commands
4. Run Terraform
    1. Update the var files in the vars directory
    2. Run `make apply-init`
5. Upload the files
    1. Download crime data from the [official site](https://data.police.uk/data/)
    2. Upload by running `make upload-data`
6. Run Terraform again to load uploaded data with `make apply-bq`
8. Create the Report with Studio

## Possible improvements

- Terraform to github CI/CD
- Add monthly triggered lambda to fetch new data and upload to google storage
- Process geographical data to produce some kind of heatmap of crimes

## TODO

- Store the terraform state in a bucket - terraform is updated, only the bucket creation is missing, make sure it is not global?
- Add some explaination for the partitioning and clustering decision 
