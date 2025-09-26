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

# ecs task execution iam role
resource "aws_iam_role" "c19_ajldka_task_execution_role" {
  name = "c19-ajldka-task-execution-role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            }
        }
    ]
})
}

# ecs task execution iam role policy
resource "aws_iam_role_policy_attachment" "c19_ajldka_task_execution_policy" {
  role= aws_iam_role.c19_ajldka_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ecs task definition
resource "aws_ecs_task_definition" "c19_ajldka_ecs_plants_task_definition" {
  family                   = "c19_ajldka_ecs_plants_task_definition"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn = aws_iam_role.c19_ajldka_task_execution_role.arn
  task_role_arn = aws_iam_role.c19_ajldka_ecs_task_role.arn
  container_definitions = jsonencode([{
        name      = "c19-ajldka-plants-dashboard"
        image     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c19-ajldka-plants-dashboard:latest"
        essential = true
        portMappings = [
        {
          containerPort = 8501
          hostPort      = 8501
          protocol      = "tcp"
        }
        ],
        environment = [
        {name = "DB_HOST", value = var.DB_HOST},
        {name = "DB_NAME", value = var.DB_NAME},
        {name = "DB_USER", value = var.DB_USER},
        {name = "DB_PASSWORD", value = var.DB_PASSWORD},
        {name = "DB_PORT", value = var.DB_PORT},
        {name = "DB_SCHEMA", value = var.DB_SCHEMA},
        {name = "DB_DRIVER", value = var.DB_DRIVER},
        {name = "AWS_ACCESS_KEY_AJLDKA", value = var.AWS_ACCESS_KEY},
        {name = "AWS_SECRET_ACCESS_KEY_AJLDKA", value = var.AWS_SECRET_ACCESS_KEY},
        {name = "AWS_REGION", value = var.AWS_REGION}
        ],
    logConfiguration = {
        logDriver = "awslogs",
        "options": {
            awslogs-group = "/ecs/c19_ajldka_ecs_plants_task_definition"
            awslogs-stream-prefix = "ecs"
            awslogs-create-group = "true"
            awslogs-region = "eu-west-2"
        }
    }
    }
  ])
  runtime_platform {
  operating_system_family = "LINUX"
  cpu_architecture        = "X86_64"
  }
}

##################################
# ecs service task iam role
resource "aws_iam_role" "c19_ajldka_ecs_task_role" {
  name = "c19-ajldka-ecs-task-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "c19_ajldka_ecs_athena" {
  role       = aws_iam_role.c19_ajldka_ecs_task_role.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonAthenaFullAccess"
}

resource "aws_iam_role_policy_attachment" "c19_ajldka_ecs_rds" {
  role       = aws_iam_role.c19_ajldka_ecs_task_role.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
}

# security group for ecs
resource "aws_security_group" "c19_ajldka_sg" {
  name        = "c19-ajldka-sg"
  description = "Allow access to Streamlit dashboard"
  vpc_id      = "vpc-0f29b6a6ab918bcd5"

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ecs service
resource "aws_ecs_service" "c19_ajldka_service" {
  name            = "c19-ajldka-service"
  cluster         = "arn:aws:ecs:eu-west-2:129033205317:cluster/c19-ecs-cluster"
  task_definition = aws_ecs_task_definition.c19_ajldka_ecs_plants_task_definition.arn
  desired_count   = "1"
  network_configuration {
    subnets          = ["subnet-00506a8db091bdf2a", "subnet-0425a4a0b929ea507", "subnet-0e7a1e60734c4fca7"]
    security_groups  = [aws_security_group.c19_ajldka_sg.id]
    assign_public_ip = true
  }
  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 100
    base              = 1
  }
  deployment_circuit_breaker {
    enable   = false
    rollback = false
  }

  deployment_configuration {
    bake_time_in_minutes = "0"
    strategy             = "ROLLING"
  }

  deployment_controller {
    type = "ECS"
  }
}