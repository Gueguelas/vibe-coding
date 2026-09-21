# AGENTS.md

## O que é este projeto
**Stable** é o app web, em português do Brasil, de empréstimo de equipamentos de
TI — notebooks, monitores, cabos, câmeras — para uso interno. Ele substitui a
planilha compartilhada onde ninguém sabe o que está disponível e devolução só é
registrada se alguém lembrar.

- **Colaborador**: vê o catálogo, solicita empréstimo de item disponível e devolve o que está com ele — vê somente os próprios empréstimos.
- **Operações**: cadastra equipamentos, vê todos os empréstimos em aberto e registra devolução no balcão.

Estado atual: este repositório contém só documentação. O código vive em dois
repositórios separados (front e API; ver docs/adr/001-stack.md).

## Comandos
Não há build nem teste neste repositório: ele é documentação. Os comandos de
teste, build e migration vivem nos repositórios de front e de API — o que
rodar antes de declarar uma tarefa pronta está em docs/rules/checks.md, e o
procedimento de schema está em docs/rules/migration.md.

Git: nunca commitar nem dar push sem pedido explícito; deixe as mudanças em
staging para revisão (ver docs/rules/RESTRICTIONS.md, seção Git).

## Estrutura
```
docs/PRD.md                → o que o negócio quer: requisitos e regras
docs/layout.md             → especificação visual (design system Nocturne:
                             acento teal do Stable, Raleway, dark) — handoff do layout
docs/adr/001-stack.md      → decisões de arquitetura e consequências
docs/rules/RESTRICTIONS.md → o que o agente não pode fazer (vale sempre)
docs/rules/checks.md       → o que precisa passar antes de dizer "pronto"
docs/rules/migration.md    → procedimento para qualquer mudança de schema
docs/handoff/              → onde a sessão parou (escrever ao fim de cada sessão)
CLAUDE.md                  → aponta para este arquivo
.env                       → ignorado pelo git — nunca versionar
.env.example               → modelo das variáveis esperadas
```

## Convenções obrigatórias
- Idioma da interface e dos docs: **PT-BR**; datas em `DD/MM/AAAA`; tom direto,
  sem exclamações, sem emoji.
- Regra de UI salva de regra de negócio: qualquer mudança de estado é derivada
  no render — contagens, KPIs, cores, rótulo e habilitação de botão; nunca
  duplicar esse estado à mão.
- Contrato front↔API atravessa via **OpenAPI gerado** (orval no front); nunca
  reescrever tipos de resposta à mão.
- Multi-tenancy desde o schema: `tenant_id` em toda tabela de domínio e
  `memberships (user_id, tenant_id, role)`; o tenant do request vem do JWT,
  resolvido no guard — nunca do body ou da query.
- O **Prisma Migrate** é o único dono do schema; RLS, policies e triggers entram
  como SQL bruto dentro das migrations, não como script solto ou segundo dono.
- Validação de entrada com **Zod** (via `nestjs-zod`), nunca `class-validator`
  — o OpenAPI sai do mesmo schema que valida.

## Rotina por tipo de tarefa
- **Qualquer tarefa**: leia docs/rules/RESTRICTIONS.md antes de começar.
- **Antes de dizer "pronto", "implementado" ou "funcionando"**: siga
  docs/rules/checks.md — testes, build, git status e o critério do PRD
  atendido, citados na resposta.
- **Qualquer mudança de schema** (tabela, coluna, índice, constraint, policy),
  mesmo trivial: siga docs/rules/migration.md — plano de DDL na resposta,
  PARE para aprovação, migration via Prisma com RLS na mesma migration,
  banco local apenas.

## O que NÃO fazer
Resumo — a fonte de verdade é docs/rules/RESTRICTIONS.md; leia-o por inteiro.
- Não commitar nem dar push sem o usuário pedir; sempre deixar em staging.
- Não criar pacote compartilhado de tipos entre front e API.
- Não escrever cliente HTTP à mão nem deixar o front falar direto com o
  Supabase — driblaria a autorização por tenant.
- Não trocar o dono do schema; adicionar `tenant_id` a tabela existente exige
  backfill e revisão de toda query.
- Não refatorar código fora do pedido atual.
- Não rodar deploy, alterar configuração da Vercel nem tocar no projeto
  Supabase remoto (SQL, schema ou dado).

## Onde olhar
- docs/PRD.md — o que o negócio quer
- docs/layout.md — como a UI deve se parecer e se comportar
- docs/adr/001-stack.md — por que decidimos assim e as consequências
- docs/rules/RESTRICTIONS.md — o que não fazer; leia antes de qualquer mexida
- docs/rules/checks.md — verificação de fim de tarefa
- docs/rules/migration.md — procedimento de mudança de schema
- docs/handoff/ — onde eu parei no desenvolvimento
