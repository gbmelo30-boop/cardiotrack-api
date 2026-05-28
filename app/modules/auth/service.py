"""
Serviço de autenticação.

Confere as credenciais do login e, dando certo, emite o token JWT. Apoia-se no
repositório de usuários (para achar a conta) e nas funções de segurança (para
conferir a senha e assinar o token). Não conhece HTTP.
"""

from app.core.security import conferir_senha, criar_token_acesso
from app.modules.auth.schemas import LoginEntrada, TokenResposta
from app.modules.usuarios.repository import RepositorioUsuarios
from app.shared.exceptions import CredenciaisInvalidas


class ServicoAuth:
    def __init__(self, repositorio: RepositorioUsuarios):
        self.repositorio = repositorio

    def autenticar(self, dados: LoginEntrada) -> TokenResposta:
        usuario = self.repositorio.buscar_por_email(dados.email)

        # Mesma mensagem para "e-mail não existe" e "senha errada": evita dar
        # pistas a quem tenta adivinhar contas.
        if usuario is None or not conferir_senha(dados.senha, usuario.senha_hash):
            raise CredenciaisInvalidas("E-mail ou senha incorretos.")

        # O 'sub' (subject) do token guarda o id do usuário, como string.
        token = criar_token_acesso({"sub": str(usuario.id)})
        return TokenResposta(token_acesso=token)
