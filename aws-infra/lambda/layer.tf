# Dependency layer defination to attach to the lambda function

resource "aws_lambda_layer_version" "lambda_layer" {
  filename            = "python.zip"
  layer_name          = "rentalAlerts"
  compatible_runtimes = ["python3.10"]
  source_code_hash = filebase64sha256("python.zip")
}