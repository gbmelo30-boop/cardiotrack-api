# CardioTrack API

Back-end do **Sistema de Acompanhamento de Saúde Cardíaca**, desenvolvido para a
disciplina de Engenharia de Software II. A API permite que um usuário crie conta,
faça login e registre/acompanhe indicadores cardíacos (pressão, frequência,
oxigenação, peso e sintomas), além de gerar relatórios com médias e histórico.

> Status: **esqueleto** do projeto. A estrutura e os contratos estão prontos; a
> lógica de cada camada é preenchida na sequência.

## Tecnologias

- **Python** com **FastAPI** (API e documentação Swagger automática)
- **SQLAlchemy** como ORM (deixa o código independente do banco)
- **PostgreSQL** em desenvolvimento, com **SQLite** como alternativa local
- **JWT** para autenticação e **bcrypt** para o hash das senhas
- **pytest** para testes unitários e de integração

## Como executar (após a implementação)

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

## Integrantes do grupo

- (preencher)
