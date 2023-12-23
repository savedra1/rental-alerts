# Environment vars form github/local 
# Must be prefaced with `TF_VAR_` when defined in env
# EG `TF_VAR_SSM_TWILIO_SID` 

variable "SSM_TWILIO_SID"       {
  type        = string
  default     = "n/a"
}

variable "SSM_TWILIO_AUTH_KEY"  {
  type        = string
  default     = "n/a"
}

variable "SSM_TWILIO_RECIPIENT" {
  type        = string
  default     = "n/a"
}

variable "SSM_TWILIO_SENDER"    {
  type        = string
  default     = "n/a"
}

variable "S3_STATE_BUCKET_NAME" {
  type        = string 
}

variable "ATLASSIAN_EMAIL_ID"   {
  type        = string 
}

variable "SMTP_SENDER_EMAIL"    {
  type        = string
}

variable "SMTP_SENDER_EMAIL"    {
  type        = string
}

variable "SMTP_SENDER_KEY"      {
  type        = string
}

variable "SMTP_RECIPIENT_EMAIL" {
  type        = string
}
########