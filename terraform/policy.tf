resource "aws_iot_policy" "device_policy" {
  name = var.device_policy_name

  policy = jsonencode({
    "Version" = "2012-10-17",
    "Statement" = [
      {
        "Effect" = "Allow",
        "Action" = [
            "iot:Connect",
            "iot:Publish",
            "iot:Subscribe",
            ]
        "Resource"= "*"
      },
    ]
  })
}