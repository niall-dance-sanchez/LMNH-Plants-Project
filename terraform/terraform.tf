terraform {
  backend "s3" {
    bucket = "c19-ajldka-terraform-state"
    key = "terraform.tfstate"
    region = "eu-west-2"
  }
}
