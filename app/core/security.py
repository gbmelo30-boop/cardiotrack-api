"""
Funções de segurança: hash de senha e tokens JWT.

Toda a parte sensível fica isolada aqui. Nenhum outro módulo precisa saber COMO
a senha é embaralhada nem COMO o token é assinado - eles apenas chamam estas
funções. Se um dia trocarmos o algoritmo, mexemos só neste arquivo.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import configuracoes


def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha em texto puro num hash seguro (bcrypt).

    O hash é de mão única: serve para conferir a senha depois, mas não há como
    voltar dele para a senha original. Por isso é o que guardamos no banco."""
    senha_em_bytes = senha.encode("utf-8")
    hash_gerado = bcrypt.hashpw(senha_em_bytes, bcrypt.gensalt())
    return hash_gerado.decode("utf-8")


def conferir_senha(senha_digitada: str, hash_salvo: str) -> bool:
    """Confere a senha do login contra o hash guardado, sem descriptografar nada.
    O próprio bcrypt refaz o cálculo e compara o resultado."""
    return bcrypt.checkpw(
        senha_digitada.encode("utf-8"), hash_salvo.encode("utf-8")
    )


def criar_token_acesso(dados: dict) -> str:
    """Gera um JWT assinado com os dados informados (normalmente o id do usuário).

    Acrescentamos o campo 'exp' (expiração): passado esse prazo, o token deixa de
    valer e o usuário precisa logar de novo."""
    conteudo = dados.copy()
    expira_em = datetime.now(timezone.utc) + timedelta(
        minutes=configuracoes.jwt_expiracao_minutos
    )
    conteudo.update({"exp": expira_em})
    return jwt.encode(
        conteudo, configuracoes.jwt_secret, algorithm=configuracoes.jwt_algoritmo
    )


def ler_token_acesso(token: str) -> dict | None:
    """Valida a assinatura e o prazo do token e devolve seu conteúdo.
    Retorna None se o token estiver adulterado ou vencido."""
    try:
        return jwt.decode(
            token, configuracoes.jwt_secret, algorithms=[configuracoes.jwt_algoritmo]
        )
    except JWTError:
        return None
