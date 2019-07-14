
variable "aws_access_key_id" {}
variable "aws_secret_access_key" {}

variable "admin_email" {}
variable "admin_password" {}

variable "ami" {
  default = "ami-02c92cda39b9bd14c" # change me / built via packer
}

variable "acme_server_url" {
  default = "https://acme-staging-v02.api.letsencrypt.org/directory"
}

variable "instance_type" {
  default = "t2.medium" # change me
}

variable "dns_root" {}

variable "dns_sub" { default = "bdns" }

variable "dns_dashboard_sub" { default = "dashbdns" }

variable "trusted_external_cidr_block" {}

variable "internet_cidr_block" {}

variable "aws_default_region" {
  default = "us-east-1"
}

variable "vpc_cidr" {
  default = "10.20.0.0/16"
}
