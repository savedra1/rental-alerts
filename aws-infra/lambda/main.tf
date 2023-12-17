# Return values from the lambda module, needed by sister modules

output "func_name" {
	value = "${aws_lambda_function.rental_alerts.function_name}"
}

output "func_arn" {
	value = "${aws_lambda_function.rental_alerts.arn}"
}