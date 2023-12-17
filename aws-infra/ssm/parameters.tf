
resource "aws_ssm_parameter" "twilio_sid" {
  name  = "/twilio/sid"
  type  = "SecureString"
  value = var.ssm_twilio_sid
}

resource "aws_ssm_parameter" "twilio_auth_key" {
  name  = "/twilio/auth_key"
  type  = "SecureString"
  value = var.ssm_twilio_auth_key
}

