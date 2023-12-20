# Dependency layer defination to attach to the lambda function

resource "aws_lambda_layer_version" "main_layer" {
  filename            = "python.zip"
  layer_name          = "rentalAlerts"
  compatible_runtimes = ["python3.12"]
  source_code_hash = filebase64sha256("python.zip") # Allow update each time TF runs
}

# Binaries for chrome driver and headless chromium package
resource "aws_lambda_layer_version" "webdriver_layer" {
  filename            = "selenium-driver.zip"
  layer_name          = "webDriver"
  compatible_runtimes = ["python3.7"]
}

# selenium layer for cf-bypass func
resource "aws_lambda_layer_version" "selenium_layer" {
  filename            = "../cf-bypass/python.zip"
  layer_name          = "selenium"
  compatible_runtimes = ["python3.7"]
}

