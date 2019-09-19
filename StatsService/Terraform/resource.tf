#--------------------------------------------------------------
# Resource: AWS Lambda
#--------------------------------------------------------------
resource "aws_lambda_function" "lambda" {
  description      = "${var.lambda_description}"
  filename         = "${var.package_file}"
  source_code_hash = "${base64sha256(file(var.package_file))}"
  function_name    = "${var.lambda_function_name}"
  handler          = "${var.lambda_handler_name}.lambda_handler"
  runtime          = "python2.7"
  role             = "${var.lambda_role}"
  timeout          = "${var.lambda_timeout_secs}"
  memory_size      = "${var.lambda_memory_mb}"
  kms_key_arn      = "${var.kms_key_arn}"

  vpc_config {
    security_group_ids = "${var.security_group_ids}"
    subnet_ids         = "${var.subnet_ids}"
  }
}

