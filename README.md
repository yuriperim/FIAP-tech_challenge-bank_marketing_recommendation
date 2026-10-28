# Bank Marketing Recommendation — Tech Challenge (Datathon)

Este projeto foi desenvolvido como proposta de solução ao Tech Challenge (Datathon), especificamente ao desafio da 5ª Fase da Pós Tech em Machine Learning Engineering. O desafio consiste em projetar uma plataforma de experimentação adaptativa para ofertas, mensagens ou próximos passos em canais digitais. Mais detalhes sobre a solução podem ser encontrados neste [vídeo](https://www.youtube.com/watch?v=Kjkvf5YbacA).

## Dataset

[Bank Marketing (Kaggle — henriqueyamahata)](https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing)

## Baseline vs Algoritmo adaptativo

- **Baseline**: política fixa, sempre utiliza o braço (arm) com maior taxa de conversão histórica (`cellular`).
- **Adaptativo**: Thompson Sampling não-contextual.

## Deploy - Produção (Nuvem AWS)

A imagem Docker da API pode ser publicada no **Amazon ECR** (registry privado) pelo workflow do **GitHub Actions** disponível neste repositório. Esse workflow se autentica na AWS por OIDC (o que elimina a necessidade de chaves de acesso armazenadas como secret). A infraestrutura necessária (repositório ECR, role IAM e provedor OIDC) pode ser provisionada via **Terraform**, e os arquivos para subir essa infraestrutura estão no diretório `infra/`.

Como proposta para a execução da imagem da API, sugere-se o uso do **AWS App Runner**, serviço gerenciado que a serve publicamente via HTTPS a partir do ECR. Este componente ainda não está provisionado neste repositório.

Requisitos:
- [git](https://git-scm.com/)
- Repositório próprio no GitHub (pode ser uma cópia deste)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), configurado com as credenciais de um usuário com as permissões necessárias
- [Terraform CLI](https://developer.hashicorp.com/terraform/install) >= 1.6

### Provisionamento da infra:
1. Clonar repositório próprio: `git clone https://github.com/<github_owner>/<github_repo>.git bank_marketing_recommendation`
2. Entrar no diretório de infraestrutura do projeto: `cd bank_marketing_recommendation/infra`
3. Criar o arquivo de variáveis a partir do modelo: `cp terraform.tfvars.example terraform.tfvars`
4. Editar o arquivo recém-criado `terraform.tfvars`, informando `github_owner` (usuário ou organização do GitHub) e `github_repo` (nome do repositório)
5. Inicializar o Terraform: `terraform init`
6. Revisar o plano de execução: `terraform plan`
7. Criar a infraestrutura: `terraform apply` (confirmar digitando `yes` quando solicitado; a flag `-auto-approve` pula a confirmação e deve ser usada com cuidado)

### Configuração GitHub Actions:
8. Obter o ARN da role que será impresso no terminal após provisionamento da infra (ou via console AWS)
9. No GitHub, acessar a aba Settings do repositório e ir em "Security and quality" > "Secrets and variables" > "Actions"; em seguida, clicar em "New repository secret"
10. Preencher com os dados: Name => `AWS_ROLE_ARN`; Secret => o ARN da role obtido no passo 8

Observações:
- O workflow `.github/workflows/ci.yml` é executado a cada push na `main` que altere ou arquivos em `api/` ou o próprio workflow, e também pode ser disparado manualmente
- Após a configuração do GitHub Actions, a primeira execução do workflow pode ser feita pelo disparo manual, ou por alguma alteração em algum arquivo da API
- Da maneira que foi configurada, a role só pode ser assumida por execuções da branch `main` do repositório informado em `terraform.tfvars`; execuções em outras branches falham na autenticação com a AWS
- As tags do ECR são imutáveis, o que significa que toda alteração que dispare o build exige uma nova versão em `api/pyproject.toml`, caso contrário o `docker push` falha
- A região (`us-east-1`) e o nome do repositório ECR (`bank-marketing-recommendation-api`) são os valores padrão do Terraform e também estão fixos no `ci.yml`, portanto se forem alterados em um, devem ser alterados no outro
- Para remover a infraestrutura, usar o comando `terraform destroy` (o repositório ECR é removido mesmo contendo imagens)

## Deploy - Desenvolvimento (local)

O projeto está dividido em duas etapas, cada uma com seu próprio ambiente: `training/`, responsável pela exploração dos dados (EDA) e treinamento do bandit, e `api/`, responsável por servir o modelo treinado via API REST.

Requisitos:
- [git](https://git-scm.com/) e [git-lfs](https://git-lfs.com/)
- [Python](https://www.python.org/) >= 3.10
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/) (opcional)

Início rápido:
1. Clonar repositório: `git clone https://github.com/yuriperim/FIAP-tech_challenge-bank_marketing_recommendation.git bank_marketing_recommendation`
2. Entrar no diretório do projeto: `cd bank_marketing_recommendation`
3. Baixar os arquivos versionados via git-lfs: `git lfs pull`

### Treinamento do modelo:
4. Entrar no diretório de treinamento: `cd training`
5. Instalar dependências: `uv sync`
6. Executar, em ordem, `notebooks/01-eda.ipynb` e `notebooks/02-baseline_vs_adaptive(thompson_sampling_no_context).ipynb` - ao final, os parâmetros do bandit são salvos em `api/artifacts/non_contextual_bandit.json`

### Execução da API (ambiente local, sem Docker):
7. Entrar no diretório da API: `cd ../api`
8. Instalar dependências: `uv sync`
9. Subir aplicação: `uv run uvicorn app.main:app --reload`
10. Acessar a documentação interativa em `http://127.0.0.1:8000/docs` e testar o endpoint `/recommend/non-contextual`

### Execução da API (ambiente local, com Docker):
7. Entrar no diretório da API: `cd ../api`
8. Construir a imagem: `docker build -t bank-marketing-recommendation-api .`
9. Subir o container: `docker run -p 8000:8000 bank-marketing-recommendation-api`
10. Acessar a documentação interativa em `http://127.0.0.1:8000/docs` e testar o endpoint `/recommend/non-contextual`

Obs.: para derrubar a aplicação, apertar `Ctrl + C`

## Principais pastas e responsabilidades
- `training/`
  - `data/raw/` — dataset original (Kaggle)
  - `notebooks/01-eda.ipynb` — análise exploratória dos dados
  - `notebooks/02-baseline_vs_adaptive(thompson_sampling_no_context).ipynb` — baseline, Thompson Sampling não-contextual, comparação, tracking via MLflow
  - `notebooks/mlflow.db` — backend de tracking do MLflow
- `api/`
  - `app/main.py` — aplicação FastAPI
  - `app/schemas/` — modelos de request/response (Pydantic)
  - `artifacts/non_contextual_bandit.json` — parâmetros do bandit treinado
  - `Dockerfile` — build da imagem da API
- `infra/` — arquivos Terraform para provisionamento da infraestrutura em Nuvem AWS

Outros arquivos importantes

- `training/pyproject.toml` — dependências do ambiente de treinamento
- `api/pyproject.toml` — dependências do ambiente da API
- `.github/workflows/ci.yml` — pipeline de lint, build e envio da imagem da API para o ECR
