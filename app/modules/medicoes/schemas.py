"""Schemas das medições: registro de entrada, item de saída e o relatório."""

from datetime import datetime

from pydantic import BaseModel


class MedicaoCriar(BaseModel):
    pressao_sistolica: int | None = None
    pressao_diastolica: int | None = None
    frequencia_cardiaca: int | None = None
    oxigenacao_sangue: int | None = None
    peso_corporal: float | None = None
    falta_de_ar: bool = False
    dor_no_peito: bool = False
    tontura: bool = False


class MedicaoResposta(MedicaoCriar):
    id: int
    registrado_em: datetime

    model_config = {"from_attributes": True}


class RelatorioSaude(BaseModel):
    """Resumo que alimenta os gráficos e o histórico no front-end.
    A API entrega os números já calculados; o app só desenha."""
    total_registros: int
    media_frequencia_cardiaca: float | None
    media_pressao_sistolica: float | None
    media_pressao_diastolica: float | None
    media_oxigenacao: float | None
    historico: list[MedicaoResposta]
