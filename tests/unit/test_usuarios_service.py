"""
Testes UNITÁRIOS do serviço de usuários.

Unitário = testa uma peça isolada. Aqui usamos um repositório "de mentira"
(fake), guardado em memória, para checar só a regra de negócio - sem banco real.
Assim validamos duas coisas: a senha vira hash e e-mail repetido é recusado.
"""

import pytest

from app.modules.usuarios.schemas import UsuarioCriar
from app.modules.usuarios.service import ServicoUsuarios
from app.shared.exceptions import EmailJaCadastrado


class RepositorioFake:
    """Imita o repositório real, mas guardando os usuários numa lista."""

    def __init__(self):
        self.usuarios = []

    def buscar_por_email(self, email):
        return next((u for u in self.usuarios if u.email == email), None)

    def salvar(self, usuario):
        usuario.id = len(self.usuarios) + 1
        self.usuarios.append(usuario)
        return usuario


def _dados(email="ana@exemplo.com"):
    return UsuarioCriar(
        nome="Ana",
        sobrenome="Souza",
        email=email,
        telefone="11999998888",
        senha="Senha123",
        confirmar_senha="Senha123",
        data_nascimento="1995-04-10",
        sexo="Feminino",
        pais_residencia="Brasil",
    )


def test_cadastro_guarda_senha_como_hash():
    servico = ServicoUsuarios(RepositorioFake())
    usuario = servico.cadastrar(_dados())

    # A senha original não pode aparecer guardada; o que fica é o hash.
    assert usuario.senha_hash != "Senha123"
    assert usuario.senha_hash.startswith("$2b$")


def test_email_repetido_e_recusado():
    servico = ServicoUsuarios(RepositorioFake())
    servico.cadastrar(_dados())

    with pytest.raises(EmailJaCadastrado):
        servico.cadastrar(_dados())  # mesmo e-mail de novo
