# Main exec role used for Lambda function

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