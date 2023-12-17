# CONFIG #################################

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

# MODULES ################################

module "lambda" {
    source = "./lambda"
}

module "cloudwatch" {
    source = "./cloudwatch"
    func_name = "${module.lambda.func_name}"
    func_arn = "${module.lambda.func_arn}"
}

module "ssm" { # Requires environment vars passed in for twilio auth information
    source = "./ssm"
    ssm_twilio_sid = var.SSM_TWILIO_SID
    ssm_twilio_auth_key = var.SSM_TWILIO_AUTH_KEY
    func_name = "${module.lambda.func_name}"
}

#####































