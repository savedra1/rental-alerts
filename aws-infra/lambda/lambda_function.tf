# main lambda function config

resource "aws_lambda_function" "rental_alerts" {
  function_name    = "rental-alerts"
  role             = aws_iam_role.lambda_exec_role2.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.7"
  timeout          = 900
  memory_size      = 1000
  layers           = [aws_lambda_layer_version.lambda_layer.arn, aws_lambda_layer_version.webdriver_layer.arn]
  filename         = "function_code.zip"
  source_code_hash = filebase64sha256("function_code.zip")
}

