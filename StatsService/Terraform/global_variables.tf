#--------------------------------------------------------------
# Global variables used by all the *.tf
# Variable files can be passed to terraform using -var-file=terraform_global.tfvars flag.
# More info: https://www.terraform.io/docs/configuration/variables.html
#--------------------------------------------------------------

variable "aws_region" {
  default = "ap-southeast-2"
}
variable "aws_profile" {
  default = "default"
}
variable "lambda_role" {
  default = "arn:aws:iam::1234567890:role/lambda-kinesis-execution-role"
}
variable "security_group_ids" {
  default = ["sg-121b0270"]
  type = "list"
}
variable "subnet_ids" {
  default = ["subnet-a9043edd"]
  type = "list"
}
variable "kms_key_arn" {
  default = "arn:aws:kms:ap-southeast-2:1234567890:key/cfc7acf7-4f20-49c3-aa11-8be4cdc3291d"
}
variable "terraform_state_s3_root" {
  description = "Root S3 bucket where all the state files are stored"
  default = "dev.terraform.state"
}


#--------------------------------------------------------------
# Write terraform state to S3 bucket
#--------------------------------------------------------------
terraform {
  backend "s3" {
    bucket = "dev.terraform.state"
    key    = "LoggingLambda/terraform.tfstate"
    region = "ap-southeast-2"
  }
}
