output "github_actions_aws_role_arn" {
  description = "Configurar secret AWS_ROLE_ARN no respectivo repo do GitHub"
  value       = aws_iam_role.github_actions.arn
}
