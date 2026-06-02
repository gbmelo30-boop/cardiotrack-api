# Arquitetura e Modularização — CardioTrack API

Documento exigido na entrega: explica como o projeto está organizado e por quê.

## 1. Visão geral

O sistema segue uma **arquitetura em camadas** organizada **por domínio**
(*feature-based*). Em vez de agrupar os arquivos por tipo (todos os "controllers"
juntos, todos os "models" juntos), agrupamos por assunto: tudo o que diz respeito
a "usuários" mora em um módulo, "autenticação" em outro, "medições" em outro.
Cada módulo é uma fatia vertical completa e quase independente.

A vantagem prática: para mexer em uma funcionalidade, você abre uma única pasta;
e cada integrante do grupo pode ficar responsável por um módulo, o que casa com a
arguição individual da avaliação.

## 2. As camadas

Dentro de cada módulo, a responsabilidade é dividida em quatro camadas, sempre na
mesma ordem de dependência (de cima para baixo):

1. **Router (HTTP)** — recebe a requisição, valida o formato de entrada e devolve
   a resposta. Não contém regra de negócio.
2. **Service (negócio)** — onde vivem as regras: validações, cálculos, decisões.
   Não conhece HTTP nem SQL.
3. **Repository (dados)** — única camada que conversa com o banco, via ORM.
4. **Models / Schemas** — *models* descrevem as tabelas; *schemas* descrevem o que
   entra e sai pela API.

O fluxo de uma requisição é sempre: `Router → Service → Repository → Banco`, e a
resposta volta pelo caminho inverso. Como cada camada só conhece a de baixo, dá
para testar e trocar peças sem efeito cascata — por exemplo, trocar PostgreSQL por
SQLite mexe só no repositório/configuração.

## 3. Por que esse desenho

- **Baixo acoplamento, alta coesão**: cada arquivo tem um motivo único para mudar.
- **Testabilidade**: como o serviço não depende de banco real, dá para testá-lo com
  um repositório falso (teste unitário); os endpoints inteiros são cobertos pelos
  testes de integração.
- **Independência de banco**: o ORM e a string de conexão isolam o SGBD, então o
  mesmo código roda em PostgreSQL ou SQLite.

## 4. Módulos

| Módulo      | Responsabilidade                                                |
|-------------|-----------------------------------------------------------------|
| `usuarios`  | Cadastro de conta e dados do usuário                            |
| `auth`      | Login e emissão do token JWT (reusa o usuário, sem tabela nova) |
| `medicoes`  | Registro das medições e geração do relatório de saúde           |

## 5. Estratégia de testes

- **Unitários** (`tests/unit`): focam nas regras de negócio dos *services*, isolados
  do banco e da rede.
- **Integração** (`tests/integration`): exercitam o fluxo real pela API (criar conta
  → login → registrar medição → relatório), usando um banco SQLite em memória.

## 6. Versionamento

O histórico do Git é construído em commits pequenos e temáticos (configuração,
módulo de usuários, autenticação, medições, testes, documentação), refletindo a
evolução incremental do projeto.
