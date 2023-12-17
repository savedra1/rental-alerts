# Environment vars form github/local 
# Must be prefaced with `TF_VAR_` when defined in env
# EG `TF_VAR_SSM_TWILIO_SID` 

variable "SSM_TWILIO_SID" {
  type        = string
}

variable "SSM_TWILIO_AUTH_KEY" {
  type        = string
}

variable "S3_STATE_BUCKET_NAME" {
  type        = string 
}

########