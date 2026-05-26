"""
Serviço de usuários (regras de negócio).

Aqui ficam as decisões: não pode haver dois e-mails iguais e a senha precisa
virar hash antes de ser salva. O serviço orquestra o repositório e a camada de
segurança, mas não conhece HTTP nem SQL.
"""

from app.core.security import gerar_hash_senha
from app.modules.usuarios.models import Usuario
from app.modules.usuarios.repository import RepositorioUsuarios
from app.modules.usuarios.schemas import UsuarioCriar
from app.shared.exceptions import EmailJaCadastrado


class ServicoUsuarios:
    def __init__(self, repositorio: RepositorioUsuarios):
        self.repositorio = repositorio

    def cadastrar(self, dados: UsuarioCriar) -> Usuario:
        # Regra 1: e-mail é a identidade de login, então não pode repetir.
        if self.repositorio.buscar_por_email(dados.email):
            raise EmailJaCadastrado("Já existe uma conta com este e-mail.")

        # Regra 2: a senha nunca é salva como texto - guardamos só o hash.
        novo_usuario = Usuario(
            nome=dados.nome,
            sobrenome=dados.sobrenome,
            email=dados.email,
            telefone=dados.telefone,
            senha_hash=gerar_hash_senha(dados.senha),
            data_nascimento=dados.data_nascimento,
            sexo=dados.sexo,
            pais_residencia=dados.pais_residencia,
        )
        return self.repositorio.salvar(novo_usuario)
