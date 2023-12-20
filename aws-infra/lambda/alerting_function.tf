# main lambda function config

resource "aws_lambda_function" "rental_alerts" {
  function_name                  = "rental-alerts"
  role                           = aws_iam_role.alerting_exec_role.arn
  handler                        = "lambda_function.lambda_handler"
  runtime                        = "python3.10"
  timeout                        = 900
  memory_size                    = 1000
  reserved_concurrent_executions = 1
  layers                         = [aws_lambda_layer_version.main_layer.arn]
  filename                       = "main_function_code.zip"
  source_code_hash               = filebase64sha256("main_function_code.zip")
}

