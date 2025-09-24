provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_ACCESS_KEY
}

resource "aws_s3_bucket" "c19_ajldka_s3_lmnh_plants" {
    bucket = "c19-ajldka-lmnh-plants"
    force_destroy = true
}

resource "aws_s3_bucket_versioning" "c19_lmnh_plants_versioning" {
  bucket = aws_s3_bucket.c19_ajldka_s3_lmnh_plants.id
  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_iam_role" "c19_ajldka_glue_role_lmnh_plants" {
  name = "c19-ajldka-glue-role-lmnh_plants"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "c19_ajldka_glue_role_attach_lmnh_plants" {
  role       = aws_iam_role.c19_ajldka_glue_role_lmnh_plants.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_glue_catalog_database" "c19_ajldka_glue_catalog_database_lmnh_plants" {
  name = "c19-ajldka-lmnh-plants-db"
}

resource "aws_glue_crawler" "c19_ajldka_glue_crawler_lmnh_plants" {
  database_name = aws_glue_catalog_database.c19_ajldka_glue_catalog_database_lmnh_plants.name
  name          = "c19-ajldka-lmnh-plants-db"
  role          = aws_iam_role.c19_ajldka_glue_role_lmnh_plants.arn

  s3_target {
    path = "s3://${aws_s3_bucket.c19_ajldka_s3_lmnh_plants.bucket}"
  }
}

