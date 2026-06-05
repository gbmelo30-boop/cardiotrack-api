# CardioTrack API

API REST para acompanhamento de saúde cardíaca. Permite que uma pessoa crie sua
conta, faça login e registre indicadores do coração — pressão arterial,
frequência cardíaca, oxigenação no sangue, peso e sintomas — gerando relatórios
com médias e histórico para acompanhar a evolução ao longo do tempo.

O projeto foi construído com foco em **organização, modularização e testes**:
uma arquitetura em camadas, separada por domínio, fácil de entender e de manter.

O repositório reúne as duas partes do sistema:

- **API (back-end)** — na raiz do projeto (`app/`, `tests/`, `docs/`).
- **App (front-end)** — em [`frontend/`](frontend/), aplicativo mobile em Ionic +
  Angular que consome a API.

## Tecnologias

- **Python** com **FastAPI** (API e documentação Swagger automática)
- **SQLAlchemy** como ORM (deixa o código independente do banco)
- **PostgreSQL** em desenvolvimento, com **SQLite** como alternativa local
- **JWT** para autenticação e **bcrypt** para o hash das senhas
- **pytest** para testes unitários e de integração

## Funcionalidades

- Cadastro de conta com validação de e-mail único e confirmação de senha
- Login com emissão de token JWT
- Registro de medições cardíacas (pressão, frequência, oxigenação, peso, sintomas)
- Histórico das medições do usuário
- Relatório com médias dos principais indicadores

## Como executar

```bash
# 1. Criar e ativar um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Configurar o ambiente
cp .env.example .env             # e ajustar a DATABASE_URL, se necessário

# 4. Subir a API
uvicorn app.main:app --reload
```

Documentação interativa (Swagger UI): http://localhost:8000/docs

## Testes

```bash
pytest
```

Os testes estão divididos entre **unitários** (regras de negócio isoladas) e de
**integração** (fluxo completo pela API).

## Estrutura do projeto

```
app/
├── core/        # configuração, conexão com o banco e segurança (JWT/hash)
├── shared/      # erros de negócio e dependências reutilizáveis
├── modules/     # uma pasta por domínio, cada uma com suas camadas
│   ├── usuarios/
│   ├── auth/
│   └── medicoes/
└── main.py      # monta a aplicação e registra os módulos
tests/
├── unit/        # testes de regras de negócio isoladas
└── integration/ # testes batendo nos endpoints da API
```

A explicação detalhada da arquitetura e da modularização está em
[`docs/ARQUITETURA.md`](docs/ARQUITETURA.md).
