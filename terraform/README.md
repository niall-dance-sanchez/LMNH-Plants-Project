# Terraform scripts 

These files are needed for all AWS resource creation.

## Setup

Add a `terraform.tfvars` file in this directory with your AWS access key and secret access key.

```
AWS_ACCESS_KEY="[your_access_key]"
AWS_SECRET_ACCESS_KEY="[your_secret_access_key]"
```

## Usage

In the terminal,
1. Run `terraform init` to initialise terraform.
2. Run `terraform plan` to see the changes.
3. Run `terraform apply` to apply these changes.
4. Run `terraform destroy` to delete all AWS resources in this file including all data in the resources.