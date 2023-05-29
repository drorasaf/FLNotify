resource "aws_cognito_user_pool" "auth" {
  name = "federated_auth"
}
