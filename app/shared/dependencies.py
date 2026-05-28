"""
Dependências reutilizáveis das rotas.

Aqui mora a verificação do token: dada uma requisição, descobrimos qual usuário
está por trás dela. Qualquer rota que precise de login é só declarar que depende
de 'usuario_autenticado' e o FastAPI cuida do resto.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import obter_sessao
from app.core.security import ler_token_acesso
from app.modules.usuarios.models import Usuario
from app.modules.usuarios.repository import RepositorioUsuarios

# O HTTPBearer faz o FastAPI esperar um cabeçalho "Authorization: Bearer <token>"
# e ainda mostra o cadeado de login no Swagger.
esquema_token = HTTPBearer()


def usuario_autenticado(
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_token),
    sessao: Session = Depends(obter_sessao),
) -> Usuario:
    """Lê o token enviado, valida e devolve o usuário correspondente.
    Se o token for inválido ou o usuário não existir mais, barra com 401."""
    erro_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    conteudo = ler_token_acesso(credenciais.credentials)
    if conteudo is None or "sub" not in conteudo:
        raise erro_401

    usuario = RepositorioUsuarios(sessao).buscar_por_id(int(conteudo["sub"]))
    if usuario is None:
        raise erro_401
    return usuario
