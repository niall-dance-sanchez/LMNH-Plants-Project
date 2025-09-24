provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_ACCESS_KEY
}

resource "aws_s3_bucket" "c19_ajldka_s3_lmnh_plants" {
    bucket = "c19-ajldka-lmnh-plants"
    force_destroy = true
}

resource "aws_s3_bucket_versioning" "c19_ajldka_lmnh_plants_versioning" {
  bucket = aws_s3_bucket.c19_ajldka_s3_lmnh_plants.id
  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_ecr_repository" "c19_ajldka_ecr_lmnh_plants" {
  name                 = "c19-ajldka-lmnh-plants"
  image_tag_mutability = "MUTABLE"
}
