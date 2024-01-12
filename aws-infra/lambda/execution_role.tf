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

# Inline policy for SSM read-only permissions
resource "aws_iam_role_policy" "ssm_read_only_policy" {
  name   = "SSMReadOnlyPolicy"
  role   = aws_iam_role.alerting_exec_role.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath",
          "ssm:List*",
          "ssm:Describe*",
          "ssm:PutParameter"
        ],
        Effect   = "Allow",
        Resource = "*",
      },
    ],
  })
}


# Cloudwatch logging perms for main lambda
resource "aws_iam_role_policy_attachment" "alerting_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.alerting_exec_role.name
}





