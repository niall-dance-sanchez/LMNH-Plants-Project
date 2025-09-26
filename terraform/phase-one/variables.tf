variable "AWS_ACCESS_KEY" {
    type = string
}

variable "AWS_SECRET_ACCESS_KEY" {
    type = string
}

variable "AWS_REGION" {
    type        = string
    default     = "eu-west-2"
}

variable DB_HOST {
    type = string
}

variable DB_PORT {
    type = number
}

variable DB_NAME {
    type = string
}

variable DB_USER {
    type = string
}

variable DB_PASSWORD {
    type = string
}

variable DB_DRIVER {
    type = string
}

variable DB_SCHEMA {
    type = string
}
