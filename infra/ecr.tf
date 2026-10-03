resource "aws_ecr_repository" "api_repository" {
  name                 = var.project_name
  image_tag_mutability = "IMMUTABLE" # proíbe reescrita de tags
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    infra_origin   = var.infra_origin
    project_origin = var.project_origin
    project_name   = var.project_name
  }
}
