
# Backend config
provider "aws" {
    region = "eu-west-1"
}

terraform {
  backend "s3" {
    bucket = "tf-state-bucket-2213"
    key    = "dev/terraform.tfstate"
    region = "eu-west-1"
  }
}

# Lambda module #########################################
# Exec policy
resource "aws_iam_role" "lambda_exec_role2" {
  name = "lambda-exec-role2"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Lambda function
resource "aws_lambda_function" "rental_alerts" {
  function_name    = "rental-alerts"
  role             = aws_iam_role.lambda_exec_role2.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.10"
  filename         = "function_code.zip"
  source_code_hash = filebase64sha256("function_code.zip")
}

# Cloudwatch ############################################
resource "aws_cloudwatch_event_rule" "lambda_trigger" {
  name        = "renal-alert-rule"
  description = "Trigger Lambda on a schedule"
  schedule_expression = "cron(0 5-21 * * ? *)"  

}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule = aws_cloudwatch_event_rule.lambda_trigger.name
  arn  = aws_lambda_function.rental_alerts.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rental_alerts.function_name
  principal     = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.lambda_trigger.arn
}

# SSM ########################################################
# Add a resource-based policy statement to allow SSM to invoke the Lambda function
resource "aws_lambda_permission" "allow_ssm" {
  statement_id  = "AllowExecutionFromSSM"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rental_alerts.function_name
  principal     = "ssm.amazonaws.com"
}

# parameters
resource "aws_ssm_parameter" "twilio_sid" {
  name  = "/twilio/sid"
  type  = "SecureString"
  value = var.SSM_TWILIO_SID
}

resource "aws_ssm_parameter" "twilio_auth_key" {
  name  = "/twilio/auth_key"
  type  = "SecureString"
  value = var.SSM_TWILIO_AUTH_KEY
}

































