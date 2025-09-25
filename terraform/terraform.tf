terraform {
  backend "s3" {
    bucket = "c19-ajldka-terraform-state"
    key = "terraform.tfstate"
    region = var.AWS_REGION
  }
}
