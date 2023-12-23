# Dependency layer defination to attach to the lambda function

resource "aws_lambda_layer_version" "main_layer" {
  filename            = "python.zip"
  layer_name          = "rentalAlerts"
  compatible_runtimes = ["python3.12"]
  source_code_hash = filebase64sha256("python.zip") # Allow update each time TF runs
}



