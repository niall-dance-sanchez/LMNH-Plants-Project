# Terraform scripts 

These terraform scripts are used to set up all AWS resources needed for deploying the LMNH plants project on the cloud.

## Setup

Add a `terraform.tfvars` file in this directory, `phase-one` and `phase-two` directory with your credentials.

```
AWS_ACCESS_KEY_AJLDKA="[your_access_key]"
AWS_SECRET_ACCESS_KEY_AJLDKA="[your_secret_access_key]"
AWS_REGION="[your_region]"

DB_HOST="[db_host]"
DB_PORT="[db_port]"
DB_USER="[db_user]"
DB_PASSWORD="[db_password]"
DB_NAME="[db_name]"
DB_SCHEMA="[db_schema]"
DB_DRIVER="[db_driver]"

```

This is to create a terraform backend for a more efficient collaboration. Skip this step if it's not needed for you.
 
 Create an S3 bucket using this if it doesn't exist already.
```
resource "aws_s3_bucket" "c19_ajldka_terraform_state" {
  bucket        = "c19-ajldka-terraform-state"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.c19_ajldka_terraform_state.id 
  versioning_configuration {
    status = "Disabled"
  }
}
```

## Usage

Make sure you're in this `terraform` directory.
1. Run `terraform init` to initialise terraform.
2. Run `terraform plan -target=module.phase-one` to see the changes.
3. Run `terraform apply -target=module.phase-one` to apply these changes.
4. 
5. Run `terraform destroy` to delete all AWS resources in this file including all data in the resources.
