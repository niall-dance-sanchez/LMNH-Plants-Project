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
  schedule      = "cron(5 0 * * ? *)"
  name          = "c19-ajldka-lmnh-plants-db"
  role          = aws_iam_role.c19_ajldka_glue_role_lmnh_plants.arn

  s3_target {
    path = "s3://${aws_s3_bucket.c19_ajldka_s3_lmnh_plants.bucket}"
  }
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "c19_ajldka_lambda_rds_etl_role_lmnh_plants" {
  name               = "c19-ajldka-lambda-rds-etl-role-lmnh-plants"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_lambda_function" "c19_ajldka_lambda_function_lmnh_plants_rds_etl" {
  function_name = "c19-ajldka-lambda-rds-etl"
  role = aws_iam_role.example.arn
  package_type = "Image"
  image_uri = "" # TODO: Slightly confused about this, we need the image URI of 
                  # the container image which we will have once it is launched, however how can 
                  # have this as a fixed value if the image uri of the container is going to change if it is launched in the future? 
  timeout = 300
  memory_size = 1024
  environment {
    variables = {
      AWS_ACCESS_KEY_AJLDKA = var.AWS_ACCESS_KEY
      AWS_SECRET_ACCESS_KEY_AJLDKA = var.AWS_SECRET_ACCESS_KEY
      DB_HOST=var.DB_HOST
      DB_PORT=var.DB_PORT
      DB_NAME=var.DB_NAME
      DB_USER=var.DB_USER
      DB_PASSWORD=var.DB_PASSWORD
      DB_DRIVER=var.DB_DRIVER
      DB_SCHEMA=var.DB_SCHEMA
    }
  }
}
