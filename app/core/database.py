"""
Conexão com o banco e base do ORM.

Concentramos aqui a criação do "engine" (a conexão de fato) e da fábrica de
sessões. Cada requisição abre uma sessão, faz seu trabalho e fecha no final -
quem cuida desse ciclo é a função obter_sessao(), usada via injeção de
dependência do FastAPI.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import configuracoes


# O SQLite exige um parâmetro extra para funcionar com várias threads.
# Esse "if" evita passar esse parâmetro quando o banco for PostgreSQL.
opcoes_conexao = {}
if configuracoes.database_url.startswith("sqlite"):
    opcoes_conexao = {"check_same_thread": False}

engine = create_engine(configuracoes.database_url, connect_args=opcoes_conexao)

# Fábrica de sessões: cada chamada a CriarSessao() devolve uma nova sessão.
CriarSessao = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Classe-mãe de todos os modelos (tabelas). O SQLAlchemy usa isso para
    saber quais tabelas existem na hora de criar o schema."""
    pass


def obter_sessao():
    """Entrega uma sessão de banco para a requisição e garante o fechamento.

    O 'yield' faz com que o FastAPI devolva a sessão para o endpoint e só
    execute o 'finally' depois que a resposta foi gerada."""
    sessao = CriarSessao()
    try:
        yield sessao
    finally:
        sessao.close()
