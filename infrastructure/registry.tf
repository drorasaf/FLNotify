resource "aws_s3_bucket" "flnotify" {
  bucket = "flnotify-thesis"
}

resource "aws_ecr_repository" "federated" {
  name                 = "federated"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
