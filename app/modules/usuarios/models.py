"""Modelo (tabela) de usuário."""

from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nome: Mapped[str] = mapped_column(String(80))
    sobrenome: Mapped[str] = mapped_column(String(80))

    # O e-mail é único: é por ele que o usuário faz login.
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    telefone: Mapped[str] = mapped_column(String(20))

    # Guardamos só o hash da senha, nunca a senha em si.
    senha_hash: Mapped[str] = mapped_column(String(255))

    data_nascimento: Mapped[date] = mapped_column(Date)
    sexo: Mapped[str] = mapped_column(String(20))
    pais_residencia: Mapped[str] = mapped_column(String(60))

    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
