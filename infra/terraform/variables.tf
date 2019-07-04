variable "dns_root" {}

variable "dns_sub" { default = "bdns" }
variable "trusted_external_cidr_block" {}

variable "internet_cidr_block" {}

variable "aws_default_region" {
  default = "us-east-1"
}

variable "vpc_cidr" {
  default = "10.20.0.0/16"
}
