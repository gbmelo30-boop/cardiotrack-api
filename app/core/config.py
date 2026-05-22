"""
Configurações centrais da aplicação.

A ideia aqui é ter um único lugar que lê as variáveis de ambiente (do arquivo
.env) e expõe tudo de forma organizada. Assim nenhum outro arquivo precisa
mexer diretamente com os.environ, o que deixa o código mais limpo e testável.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):
    # Endereço de conexão do banco. Trocar de PostgreSQL para SQLite é só
    # mudar esta string no .env - o restante do código nem percebe.
    database_url: str = "sqlite:///./cardiotrack.db"

    # Chave usada para assinar os tokens JWT. Tem que ser secreta.
    jwt_secret: str = "chave-de-desenvolvimento-apenas"
    jwt_expiracao_minutos: int = 120

    # Algoritmo de assinatura do token. HS256 é simétrico e suficiente aqui.
    jwt_algoritmo: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Instância única usada em todo o projeto (importe "configuracoes" onde precisar).
configuracoes = Configuracoes()
