resource "aws_lambda_permission" "allow_ssm" {
  statement_id  = "AllowExecutionFromSSM"
  action        = "lambda:InvokeFunction"
  function_name = var.func_name
  principal     = "ssm.amazonaws.com"
}
