"""
Erros de negócio próprios da aplicação.

Em vez de espalhar HTTPException pelas regras de negócio (o que misturaria a
camada de serviço com detalhes de HTTP), criamos exceções com significado
próprio. A camada de API depois traduz cada uma para o status code certo.
"""


class ErroDeNegocio(Exception):
    """Erro base. Todas as exceções da aplicação herdam desta."""


class RecursoNaoEncontrado(ErroDeNegocio):
    """Usado quando algo que deveria existir não foi achado (ex.: usuário)."""


class CredenciaisInvalidas(ErroDeNegocio):
    """E-mail ou senha incorretos no login."""


class EmailJaCadastrado(ErroDeNegocio):
    """Tentativa de criar conta com um e-mail que já existe."""
