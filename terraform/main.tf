provider "aws" {
    region = var.AWS_REGION
}

resource "aws_s3_bucket" "c19_lmnh_plants" {
    bucket = "c19-lmnh-plants"
    force_destroy = true
}

resource "aws_s3_bucket_versioning" "c19_lmnh_plants_versioning" {
  bucket = aws_s3_bucket.c19_lmnh_plants.id
  versioning_configuration {
    status = "Disabled"
  }
}