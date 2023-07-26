# EKS Cluster Info Retriever

This Python script is designed to retrieve and export worker node details from Amazon Elastic Kubernetes Service (EKS) clusters and save them in an Excel workbook. The script utilizes the Boto3 library to interact with AWS EKS and EC2 services and the openpyxl library to handle Excel workbook operations.

## Prerequisites

1. Python 3.x installed on your system.
2. Boto3 library for AWS interactions: pip install boto3
3. openpyxl library for working with Excel files: pip install openpyxl


## Script Overview

The script performs the following tasks:

1. Retrieves a list of EKS clusters using the `boto3.client('eks')` API.
2. For each cluster, retrieves relevant details such as cluster version and AppID (if available) using the `describe_cluster()` API.
3. Fetches worker nodes running on each cluster using the `describe_instances()` API from the `ec2_client`.
4. Extracts worker node information, including Instance ID, Instance Type, OS, and Owner (if specified using an EC2 tag).
5. Creates an Excel workbook and adds a sheet named "Worker Node Details."
6. Populates the Excel workbook with the collected information for each worker node in the cluster.
7. Saves the Excel workbook as `worker_nodes_details.xlsx` in the current working directory.

**Note:**

- The script assumes that you have proper IAM permissions to access EKS and EC2 resources in your AWS account.
- If no worker nodes are found in a cluster, the script will include "N/A" values for the worker node information in the Excel workbook.

