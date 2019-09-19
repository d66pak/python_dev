#--------------------------------------------------------------
# Variables
#--------------------------------------------------------------
variable "lambda_description" {
  description = "Lambda description"
  default = "Lambda to test custom monitoring and diagnostic logging"
}
variable "lambda_handler_name" {
  description = "Lambda handler class name"
  default = "Lambda"
}
variable "lambda_timeout_secs" {
  description = "Lambda function timeout in seconds"
  default = 300
}
variable "lambda_memory_mb" {
  description = "Lambda memory in MBs"
  default = 128
}

variable "lambda_function_name" {
  description = "Function name of lambda"
  type = "string"
}
variable "package_file" {
  description = "Zip package file path"
  type = "string"
}
