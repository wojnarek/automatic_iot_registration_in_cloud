resource "aws_iot_provisioning_template" "provision_template" {
  name                  = "JITPProvisioning"
  description           = "My provisioning template"
  provisioning_role_arn = aws_iam_role.jitp_role.arn
  enabled               = true

  template_body = jsonencode({
    Parameters = {
      SerialNumber = { Type = "String" }
    }

    Resources = {
      certificate = {
        Properties = {
          CertificateId = { Ref = "AWS::IoT::Certificate::Id" }
          Status        = "Active"
        }
        Type = "AWS::IoT::Certificate"
      }

      policy = {
        Properties = {
          PolicyName = aws_iot_policy.device_policy.name
        }
        Type = "AWS::IoT::Policy"
      }
    }
  })
}