# Cron schedule event definition

resource "aws_cloudwatch_event_rule" "lambda_trigger" {
  state               = var.state
  name                = "renal-alert-rule"
  description         = "Trigger Lambda on a schedule"
  schedule_expression = "cron(0 5-21 * * ? *)"
}
