"""
Rotas das medições.

Todas exigem usuário autenticado: cada um só vê e registra os próprios dados.
O usuário logado vem do token (via 'usuario_autenticado'), então não há como
um usuário acessar as medições de outro.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import obter_sessao
from app.modules.medicoes.repository import RepositorioMedicoes
from app.modules.medicoes.schemas import (
    MedicaoCriar,
    MedicaoResposta,
    RelatorioSaude,
)
from app.modules.medicoes.service import ServicoMedicoes
from app.modules.usuarios.models import Usuario
from app.shared.dependencies import usuario_autenticado

roteador = APIRouter(prefix="/medicoes", tags=["Saúde Cardíaca"])


def _servico(sessao: Session) -> ServicoMedicoes:
    # Pequeno atalho para montar o serviço com seu repositório.
    return ServicoMedicoes(RepositorioMedicoes(sessao))


@roteador.post("", response_model=MedicaoResposta, status_code=status.HTTP_201_CREATED)
def registrar_medicao(
    dados: MedicaoCriar,
    usuario: Usuario = Depends(usuario_autenticado),
    sessao: Session = Depends(obter_sessao),
):
    """Registra uma nova medição (tela 'Acompanhamento da Saúde Cardíaca')."""
    return _servico(sessao).registrar(usuario.id, dados)


@roteador.get("", response_model=list[MedicaoResposta])
def listar_historico(
    usuario: Usuario = Depends(usuario_autenticado),
    sessao: Session = Depends(obter_sessao),
):
    """Lista o histórico de medições do usuário logado."""
    return _servico(sessao).listar(usuario.id)


@roteador.get("/relatorio", response_model=RelatorioSaude)
def obter_relatorio(
    usuario: Usuario = Depends(usuario_autenticado),
    sessao: Session = Depends(obter_sessao),
):
    """Devolve o relatório com médias e histórico (tela 'Relatório')."""
    return _servico(sessao).gerar_relatorio(usuario.id)
