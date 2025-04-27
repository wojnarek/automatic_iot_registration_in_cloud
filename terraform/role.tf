resource "aws_iam_role" "jitp_role" {
  name = var.role_name

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "iot.amazonaws.com"
                ]
            },
            "Action": [
                "sts:AssumeRole"
            ]
        }
    ]
  })

  tags = {
    tag-key = "tag-value"
  }
}

locals {
  iot_policies = {
    "register_thing_attachmnets" = "arn:aws:iam::aws:policy/service-role/AWSIoTThingsRegistration"
    "iot_logging_attachment" = "arn:aws:iam::aws:policy/service-role/AWSIoTLogging"
    iot_rule_actions_attachment = "arn:aws:iam::aws:policy/service-role/AWSIoTRuleActions"
  }
}

resource "aws_iam_role_policy_attachment" "iot_policy_attachments" {

  for_each = local.iot_policies

  role      = aws_iam_role.jitp_role.name
  policy_arn = each.value
}