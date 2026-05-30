"""
Ponto de partida da aplicação.

Este arquivo só "monta" a API: cria o app FastAPI, registra os roteadores de
cada módulo e prepara o banco. A regra é manter este arquivo enxuto - ele
conecta as peças, mas não contém lógica de negócio.

Com a API no ar, a documentação Swagger fica em:  http://localhost:8000/docs
"""

from fastapi import FastAPI

from app.core.database import Base, engine
from app.modules.usuarios.router import roteador as roteador_usuarios
from app.modules.auth.router import roteador as roteador_auth
from app.modules.medicoes.router import roteador as roteador_medicoes

# Cria as tabelas no banco caso ainda não existam. Em um projeto maior isso
# ficaria a cargo de uma ferramenta de migração (ex.: Alembic), mas para o
# escopo do trabalho criar direto pelo ORM é suficiente e transparente.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CardioTrack API",
    description="Sistema de Acompanhamento de Saúde Cardíaca - Engenharia de Software II",
    version="0.1.0",
)

# Cada módulo expõe seu próprio roteador; aqui eles são plugados na aplicação.
app.include_router(roteador_usuarios)
app.include_router(roteador_auth)
app.include_router(roteador_medicoes)


@app.get("/", tags=["Status"])
def raiz():
    """Rota simples para checar rapidamente se a API está no ar."""
    return {"status": "ok", "mensagem": "CardioTrack API rodando"}
