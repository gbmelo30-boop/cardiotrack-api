"""
Configuração compartilhada dos testes.

Aqui ficam os 'fixtures' do pytest: pedaços de preparação reaproveitados pelos
testes. Montamos um banco SQLite em memória (rápido e descartável) e trocamos a
conexão real por ele, para que nenhum teste toque no banco de verdade.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, obter_sessao
from app.main import app


@pytest.fixture
def sessao():
    """Cria um banco em memória novinho para cada teste e o entrega.
    Usar StaticPool faz a mesma conexão ser reaproveitada, o que é necessário
    para o SQLite em memória enxergar as tabelas durante todo o teste."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    Fabrica = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    sessao_local = Fabrica()
    try:
        yield sessao_local
    finally:
        sessao_local.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def cliente(sessao):
    """Devolve um cliente HTTP que conversa com a API usando o banco de teste.
    A linha do 'dependency_overrides' diz ao FastAPI: nas rotas, use a sessão de
    teste no lugar da conexão real."""
    app.dependency_overrides[obter_sessao] = lambda: sessao
    with TestClient(app) as cliente_teste:
        yield cliente_teste
    app.dependency_overrides.clear()
