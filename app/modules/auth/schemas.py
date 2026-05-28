"""Schemas de autenticação: o que entra no login e o token que sai."""

from pydantic import BaseModel, EmailStr


class LoginEntrada(BaseModel):
    email: EmailStr
    senha: str


class TokenResposta(BaseModel):
    token_acesso: str
    tipo_token: str = "bearer"
