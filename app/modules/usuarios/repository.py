"""
Repositório de usuários (acesso ao banco).

Esta é a única camada que fala "SQL" (via ORM). Quem está acima - o serviço -
pede "busque o usuário pelo e-mail" e não precisa saber como isso é feito. Isso
facilita os testes e, no futuro, trocar a tecnologia de banco.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.usuarios.models import Usuario


class RepositorioUsuarios:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def buscar_por_email(self, email: str) -> Usuario | None:
        consulta = select(Usuario).where(Usuario.email == email)
        return self.sessao.scalar(consulta)

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        return self.sessao.get(Usuario, usuario_id)

    def salvar(self, usuario: Usuario) -> Usuario:
        # Adiciona, confirma a transação e recarrega para já ter o id gerado.
        self.sessao.add(usuario)
        self.sessao.commit()
        self.sessao.refresh(usuario)
        return usuario
