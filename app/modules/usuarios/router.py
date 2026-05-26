"""
Rotas de usuários (camada HTTP).

A porta de entrada: recebe a requisição, chama o serviço e devolve a resposta no
formato certo. A lógica de verdade fica nas camadas de baixo; aqui só traduzimos
erros de negócio para os status codes adequados.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import obter_sessao
from app.modules.usuarios.repository import RepositorioUsuarios
from app.modules.usuarios.schemas import UsuarioCriar, UsuarioResposta
from app.modules.usuarios.service import ServicoUsuarios
from app.shared.exceptions import EmailJaCadastrado

roteador = APIRouter(prefix="/usuarios", tags=["Usuários"])


@roteador.post("", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
def criar_conta(dados: UsuarioCriar, sessao: Session = Depends(obter_sessao)):
    """Cria a conta do usuário (tela 'Criar Conta')."""
    servico = ServicoUsuarios(RepositorioUsuarios(sessao))
    try:
        return servico.cadastrar(dados)
    except EmailJaCadastrado as erro:
        # Traduz o erro de negócio para um 409 (conflito) com mensagem clara.
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro))
