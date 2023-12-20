# Function that exists with the purpose to only bypass 

resource "aws_lambda_function" "cf_bypass" {
  function_name                  = "cf-bypass"
  role                           = aws_iam_role.cf_bypass_exec_role.arn
  handler                        = "lambda_function.lambda_handler"
  runtime                        = "python3.7"
  timeout                        = 300
  memory_size                    = 1000
  reserved_concurrent_executions = 1
  layers                         = [aws_lambda_layer_version.selenium_layer.arn, aws_lambda_layer_version.webdriver_layer.arn]
  filename                       = "function_code.zip"
  source_code_hash               = filebase64sha256("function_code.zip")
}