"""
Schemas do usuário (Pydantic).

Schema é o "contrato" de entrada e saída da API. Separar o que ENTRA do que
SAI é importante: a senha entra no cadastro, mas nunca deve sair numa resposta.
"""

from datetime import date

from pydantic import BaseModel, EmailStr, field_validator


class UsuarioCriar(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr
    telefone: str
    senha: str
    confirmar_senha: str
    data_nascimento: date
    sexo: str
    pais_residencia: str

    @field_validator("confirmar_senha")
    @classmethod
    def senhas_devem_coincidir(cls, valor, info):
        # Garante, já na entrada, que "senha" e "confirmar senha" são iguais.
        if "senha" in info.data and valor != info.data["senha"]:
            raise ValueError("As senhas não coincidem.")
        return valor


class UsuarioResposta(BaseModel):
    # Repare: nenhum campo de senha aqui. O que vai para o cliente é só isto.
    id: int
    nome: str
    sobrenome: str
    email: EmailStr

    model_config = {"from_attributes": True}
