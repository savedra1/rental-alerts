# Permission that allows the rule access to the lambda function 
resource "aws_lambda_permission" "allow_cloudwatch_trigger" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = var.func_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_trigger.arn
}

# Define Lambda Permission for sending logs to CloudWatch
resource "aws_lambda_permission" "allow_cloudwatch_logs" {
  statement_id  = "AllowLoggingToCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = var.func_name
  principal     = "logs.amazonaws.com"
  source_arn    = aws_cloudwatch_log_group.rental_alert_logs.arn
}