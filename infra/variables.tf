variable "aws_region" {
  default = "us-east-1"
}

variable "infra_origin" {
  description = "Origem da infraestrutura"
  type        = string
  default     = "terraform"
}

variable "project_origin" {
  description = "Origem do projeto"
  type        = string
  default     = "fiap-tech_challenge"
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "bank-marketing-recommendation-api"
}

variable "github_owner" {
  description = "Usuário GitHub"
  type        = string
}

variable "github_repo" {
  description = "Repositório GitHub"
  type        = string
}
