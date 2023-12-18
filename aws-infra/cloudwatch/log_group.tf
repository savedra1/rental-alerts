
resource "aws_cloudwatch_log_group" "rental_alert_logs" {
  name              = "/aws/lambda/${var.func_name}"
  retention_in_days = 7 
}