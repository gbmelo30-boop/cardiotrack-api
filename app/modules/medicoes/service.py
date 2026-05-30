"""
Serviço das medições.

Faz dois trabalhos: registrar uma nova medição e montar o relatório (médias e
histórico) a partir de tudo que o usuário já registrou. O cálculo das médias
fica aqui, na regra de negócio - não na rota nem no banco.
"""

from app.modules.medicoes.models import Medicao
from app.modules.medicoes.repository import RepositorioMedicoes
from app.modules.medicoes.schemas import MedicaoCriar, RelatorioSaude


def _media(valores: list) -> float | None:
    """Calcula a média ignorando registros vazios (None).

    Ex.: se o usuário nem sempre anota a oxigenação, só entram na conta os dias
    em que ele realmente anotou. Sem nenhum valor, devolvemos None."""
    presentes = [v for v in valores if v is not None]
    if not presentes:
        return None
    return round(sum(presentes) / len(presentes), 1)


class ServicoMedicoes:
    def __init__(self, repositorio: RepositorioMedicoes):
        self.repositorio = repositorio

    def registrar(self, usuario_id: int, dados: MedicaoCriar) -> Medicao:
        nova = Medicao(usuario_id=usuario_id, **dados.model_dump())
        return self.repositorio.salvar(nova)

    def listar(self, usuario_id: int) -> list[Medicao]:
        return self.repositorio.listar_por_usuario(usuario_id)

    def gerar_relatorio(self, usuario_id: int) -> RelatorioSaude:
        registros = self.repositorio.listar_por_usuario(usuario_id)
        return RelatorioSaude(
            total_registros=len(registros),
            media_frequencia_cardiaca=_media([r.frequencia_cardiaca for r in registros]),
            media_pressao_sistolica=_media([r.pressao_sistolica for r in registros]),
            media_pressao_diastolica=_media([r.pressao_diastolica for r in registros]),
            media_oxigenacao=_media([r.oxigenacao_sangue for r in registros]),
            historico=registros,
        )
