# Main exec role used for Lambda function
resource "aws_iam_role" "alerting_exec_role" {
  name = "alerting_lambda_exec_role"

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

# Cloudwatch logging perms for main lambda
resource "aws_iam_role_policy_attachment" "alerting_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.alerting_exec_role.name
}

# Custom CF bypass function  exec role
resource "aws_iam_role" "cf_bypass_exec_role" {
  name = "cf_bypass_lambda_exec_role"

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

# Cloudwatch logging perms for main lambda
resource "aws_iam_role_policy_attachment" "cf_bypass_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.cf_bypass_exec_role.name
}

# Policy that allows the main function to invoke the CF bypass 
# without leaving the AWS Network
resource "aws_lambda_permission" "allow_native_invocation" {
  statement_id  = "AllowNativeInvocation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cf_bypass.arn
  principal     = aws_lambda_function.rental_alerts.arn
}

