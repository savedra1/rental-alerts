# Define the target of the clpudwatch event rule

#Commenting to disable
resource "aws_cloudwatch_event_target" "lambda_target" {
  count = var.active ? 1 : 0
  rule = aws_cloudwatch_event_rule.lambda_trigger.name
  arn  = var.func_arn
}