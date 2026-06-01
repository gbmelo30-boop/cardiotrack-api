"""
Testes de INTEGRAÇÃO da API.

Integração = exercita as camadas juntas (rota + serviço + repositório + banco de
teste), batendo nos endpoints como um cliente real faria. Cobrimos o fluxo
principal e também as proteções (rota sem token e login errado).
"""

DADOS_CONTA = {
    "nome": "Carlos",
    "sobrenome": "Lima",
    "email": "carlos@exemplo.com",
    "telefone": "21988887777",
    "senha": "Forte123",
    "confirmar_senha": "Forte123",
    "data_nascimento": "1990-08-22",
    "sexo": "Masculino",
    "pais_residencia": "Brasil",
}


def _logar(cliente):
    """Cria a conta, faz login e devolve o cabeçalho de autorização pronto."""
    cliente.post("/usuarios", json=DADOS_CONTA)
    resposta = cliente.post(
        "/auth/login",
        json={"email": DADOS_CONTA["email"], "senha": DADOS_CONTA["senha"]},
    )
    token = resposta.json()["token_acesso"]
    return {"Authorization": f"Bearer {token}"}


def test_fluxo_completo_conta_login_medicao_relatorio(cliente):
    cabecalho = _logar(cliente)

    # Registra duas medições para o relatório ter o que calcular.
    cliente.post(
        "/medicoes",
        json={"frequencia_cardiaca": 70, "pressao_sistolica": 120, "pressao_diastolica": 80},
        headers=cabecalho,
    )
    cliente.post(
        "/medicoes",
        json={"frequencia_cardiaca": 80, "pressao_sistolica": 130, "pressao_diastolica": 90},
        headers=cabecalho,
    )

    relatorio = cliente.get("/medicoes/relatorio", headers=cabecalho).json()
    assert relatorio["total_registros"] == 2
    assert relatorio["media_frequencia_cardiaca"] == 75.0  # (70 + 80) / 2


def test_email_duplicado_retorna_conflito(cliente):
    cliente.post("/usuarios", json=DADOS_CONTA)
    resposta = cliente.post("/usuarios", json=DADOS_CONTA)
    assert resposta.status_code == 409


def test_login_com_senha_errada_retorna_401(cliente):
    cliente.post("/usuarios", json=DADOS_CONTA)
    resposta = cliente.post(
        "/auth/login",
        json={"email": DADOS_CONTA["email"], "senha": "errada"},
    )
    assert resposta.status_code == 401


def test_rota_protegida_sem_token_e_bloqueada(cliente):
    resposta = cliente.get("/medicoes", headers={})
    assert resposta.status_code in (401, 403)
