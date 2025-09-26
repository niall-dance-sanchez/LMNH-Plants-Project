# provide aws key credentials
provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_ACCESS_KEY
}

# short-term etl iam role for lambda service
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

# short-term etl iam role for lambda 
resource "aws_iam_role" "c19_ajldka_lambda_rds_etl_role_lmnh_plants" {
  name               = "c19-ajldka-lambda-rds-etl-role-lmnh-plants"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# short-term etl iam role for lambda policies
resource "aws_iam_role_policy_attachment" "c19_ajldka_rds_etl_role_attach_lmnh_plants" {
  role       = aws_iam_role.c19_ajldka_lambda_rds_etl_role_lmnh_plants.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# short-term etl lambda function
resource "aws_lambda_function" "c19_ajldka_lambda_function_lmnh_plants_rds_etl" {
  function_name = "c19-ajldka-lambda-rds-etl"
  role = aws_iam_role.c19_ajldka_lambda_rds_etl_role_lmnh_plants.arn
  package_type = "Image"
  image_uri = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c19-ajldka-lmnh-plants:latest" 
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

# long-term etl iam role for lambda
resource "aws_iam_role" "c19_ajldka_lambda_s3_etl_role_lmnh_plants" {
  name = "c19-ajldka-lambda-s3-etl-role-lmnh-plants"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# long-term etl iam role for lambda policies
resource "aws_iam_role_policy_attachment" "c19_ajldka_s3_etl_role_attach_lmnh_plants" {
  role       = aws_iam_role.c19_ajldka_lambda_s3_etl_role_lmnh_plants.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# long-term etl lambda function
resource "aws_lambda_function" "c19_ajldka_lambda_function_lmnh_plants_s3_etl" {
  function_name = "c19-ajldka-lambda-s3-etl"
  role = aws_iam_role.c19_ajldka_lambda_s3_etl_role_lmnh_plants.arn
  package_type = "Image"
  image_uri = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c19-ajldka-lmnh-plants-s3:latest" 
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

# eventbridge iam role for short-term etl 
resource "aws_iam_role" "c19_ajldka_short_term_etl_scheduler_role" {
  name = "c19-ajldka-short-term-etl-scheduler-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
      }
    ]
  })
}

# eventbridge iam policy for short-term etl 
resource "aws_iam_role_policy_attachment" "c19_ajldka_short_term_etl_scheduler_role_attach" {
  role       = aws_iam_role.c19_ajldka_short_term_etl_scheduler_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaRole"
}

# eventbridge scheduler for short-term etl
resource "aws_scheduler_schedule" "c19_ajldka_short_term_etl_scheduler" {
  name        = "c19-ajldka-short-term-etl-scheduler"
  description = "Run short-term ETL job every minute."

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = "cron(* * * * ? *)"
  schedule_expression_timezone = "UTC"

  target {
    arn      = aws_lambda_function.c19_ajldka_lambda_function_lmnh_plants_rds_etl.arn
    role_arn = aws_iam_role.c19_ajldka_short_term_etl_scheduler_role.arn
  }
}

############################
# eventbridge iam role for long-term etl
resource "aws_iam_role" "c19_ajldka_long_term_etl_scheduler_role" {
  name = "c19-ajldka-long-term-etl-scheduler-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
      }
    ]
  })
}

# eventbridge iam policy for long-term etl 
resource "aws_iam_role_policy_attachment" "c19_ajldka_long_term_etl_scheduler_role_attach" {
  role       = aws_iam_role.c19_ajldka_long_term_etl_scheduler_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaRole"
}

# eventbridge scheduler for long-term etl
resource "aws_scheduler_schedule" "c19_ajldka_long_term_etl_scheduler" {
  name        = "c19-ajldka-long-term-etl-scheduler"
  description = "Run long-term ETL job every day at midnight."

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = "cron(0 0 * * ? *)"
  schedule_expression_timezone = "UTC"

  target {
    arn      = aws_lambda_function.c19_ajldka_lambda_function_lmnh_plants_s3_etl.arn 
    role_arn = aws_iam_role.c19_ajldka_long_term_etl_scheduler_role.arn 
  }
}
