"""Repositório das medições (acesso ao banco)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.medicoes.models import Medicao


class RepositorioMedicoes:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def salvar(self, medicao: Medicao) -> Medicao:
        self.sessao.add(medicao)
        self.sessao.commit()
        self.sessao.refresh(medicao)
        return medicao

    def listar_por_usuario(self, usuario_id: int) -> list[Medicao]:
        # Mais recentes primeiro: é a ordem natural para histórico e gráficos.
        consulta = (
            select(Medicao)
            .where(Medicao.usuario_id == usuario_id)
            .order_by(Medicao.registrado_em.desc())
        )
        return list(self.sessao.scalars(consulta))
