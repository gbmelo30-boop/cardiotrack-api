"""
Modelo das medições cardíacas.

Cada linha é um registro feito pelo usuário num dado momento: pressão,
frequência, oxigenação, peso e os sintomas marcados. Tudo é opcional fora a
ligação com o usuário e a data, porque o usuário pode registrar só parte.
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Medicao(Base):
    __tablename__ = "medicoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # A qual usuário este registro pertence.
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)

    # Pressão arterial costuma ser anotada como dois números (sistólica/diastólica).
    pressao_sistolica: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pressao_diastolica: Mapped[int | None] = mapped_column(Integer, nullable=True)

    frequencia_cardiaca: Mapped[int | None] = mapped_column(Integer, nullable=True)
    oxigenacao_sangue: Mapped[int | None] = mapped_column(Integer, nullable=True)
    peso_corporal: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Sintomas como marcações de sim/não.
    falta_de_ar: Mapped[bool] = mapped_column(Boolean, default=False)
    dor_no_peito: Mapped[bool] = mapped_column(Boolean, default=False)
    tontura: Mapped[bool] = mapped_column(Boolean, default=False)

    registrado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
