# Bank Marketing Recommendation — Tech Challenge (Datathon)

Este projeto foi desenvolvido como proposta de solução ao Tech Challenge (Datathon), especificamente ao desafio da 5ª Fase da Pós Tech em Machine Learning Engineering. O desafio consiste em projetar uma plataforma de experimentação adaptativa para ofertas, mensagens ou próximos passos em canais digitais. Mais detalhes sobre a solução podem ser encontrados neste [vídeo](https://www.youtube.com/watch?v=Kjkvf5YbacA).

## Dataset

[Bank Marketing (Kaggle — henriqueyamahata)](https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing)

## Baseline vs Algoritmo adaptativo

- **Baseline**: política fixa, sempre utiliza o braço (arm) com maior taxa de conversão histórica (`cellular`).
- **Adaptativo**: Thompson Sampling não-contextual.

## Deploy - Produção (Nuvem AWS)

Como proposta de deploy, sugere-se o uso do **Amazon ECR** como registry privado das imagens Docker da API e do **AWS App Runner** como serviço gerenciado para servi-las publicamente via HTTPS. A publicação da imagem poderia ser automatizada via GitHub Actions, autenticando-se na AWS por OIDC (sem chaves de acesso armazenadas como secret).

A infraestrutura pode ser provisionada via Terraform (IaC).

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

Outros arquivos importantes

- `training/pyproject.toml` — dependências do ambiente de treinamento
- `api/pyproject.toml` — dependências do ambiente da API
