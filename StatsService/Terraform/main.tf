#--------------------------------------------------------------
# Read terraform state from S3 bucket
#--------------------------------------------------------------
data "terraform_remote_state" "network" {
  backend = "s3"
  config {
    bucket  = "${var.terraform_state_s3_root}"
    key     = "${var.lambda_function_name}/terraform.tfstate"
    region  = "${var.aws_region}"
    encrypt = true
  }
}
