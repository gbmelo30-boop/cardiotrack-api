"""Rotas de autenticação (login)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import obter_sessao
from app.modules.auth.schemas import LoginEntrada, TokenResposta
from app.modules.auth.service import ServicoAuth
from app.modules.usuarios.repository import RepositorioUsuarios
from app.shared.exceptions import CredenciaisInvalidas

roteador = APIRouter(prefix="/auth", tags=["Autenticação"])


@roteador.post("/login", response_model=TokenResposta)
def login(dados: LoginEntrada, sessao: Session = Depends(obter_sessao)):
    """Faz login com e-mail e senha e devolve o token de acesso."""
    servico = ServicoAuth(RepositorioUsuarios(sessao))
    try:
        return servico.autenticar(dados)
    except CredenciaisInvalidas as erro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(erro)
        )
