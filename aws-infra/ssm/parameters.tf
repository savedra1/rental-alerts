
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

resource "aws_ssm_parameter" "twilio_recipient" {
  name  = "/twilio/recipient"
  type  = "SecureString"
  value = var.ssm_twilio_recipient
}

resource "aws_ssm_parameter" "twilio_sender" {
  name  = "/twilio/sender"
  type  = "SecureString"
  value = var.ssm_twilio_sender
}

resource "aws_ssm_parameter" "atlassian_id" {
  name  = "/atlassian/email_id"
  type  = "SecureString"
  value = var.atlassian_email_id
}


