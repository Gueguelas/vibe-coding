# Tasks — 001-fundacao-front

Derivado de `plan.md`. Uma tarefa por vez; ao terminar, `rules/checks.md`
(`npm run test`, `npm run build`, `git status --short`, citação do CA).
Commit só com pedido explícito, conforme `rules/RESTRICTIONS.md` e
`rules/operacoes.md`. Os estados abaixo descrevem a presença do código em
05/11/2026; não são aprovação de CA nem registro de checks executados nesta
atualização.
CA: **01** login · **02** catálogo · **03** solicitar ·
**04** devolver · **05** Operações · **06** limite 3 · **07** prazo 14 ·
**08** atraso bloqueia · **09** manutenção · **10** escopo por pessoa.

> Dependências com nível "pedir antes" (`operacoes.md`): instalação dos
> pacotes da tarefa 1. As demais tarefas da fundação criam arquivos
> ("avisar depois") sobre essa base.

| # | Tarefa | CA | Checks | Estado observado |
|---|---|---|---|---|
| 1 | Scaffold: `package.json`, `tsconfig` strict, Vite + alias `@/`, ESLint + Prettier, Vitest + jsdom, `index.html` com Raleway, `main.tsx`, `.gitignore` | 01 (pré-condição de todos) | `npm run build`, `npm run test`, `git status` | Implementado; checks precisam ser executados para aceite formal |
| 2 | Design system: tokens `@theme` do ADR-002 (cores, rampa teal, raios, escala, tipografia), base de reset, keyframes `fadeUp` | 02, 03, 04, 05 (pré-condição visual) | build + teste de tokens | Parcial; tokens principais existem, medidas pontuais diferem do ADR-002 |
| 3 | Primitivos de UI: botão, input, dialog, toast, pills, filtros, avatar — conforme ADR-002 §5 | 02, 03, 04, 05 | build + testes de render por variante | Implementado no código; verificar aderência visual e checks |
| 4 | Regras derivadas: situação, bloqueio (limite/atraso), KPIs, prazo 14 dias, `DD/MM/AAAA`, atraso | 06, 07, 08, 09, 10 | testes Vitest `test_ca_06…test_ca_10` | Parcial; funções e testes existem, mas as telas usam dados em memória |
| 5 | Sessão: `supabase-js`, loader e guards de sessão/papel; papel fornecido por `GET /v1/sessao` | 01, 10 | testes dos guards (sem sessão → login; papel errado → redirect) | Parcial e divergente: front lê claims; rota de sessão não existe |
| 6 | Shell: barra sticky, abas por papel, tag, avatar, sair; rotas + outlet conforme plan §2 | 01, 10 | testes: abas de colaborador × Operações | Implementado no código; validar checks para aceite formal |
| 7 | Página de login (ADR-002 §6.1): e-mail/senha via RHF+Zod, redirecionamento, erros via toast | 01 | testes do form; Playwright cobre login de demonstração | Implementado; o atalho de Operações só existe sem Supabase configurado |
| 8 | API (dependência): `GET /v1/sessao` + expor `openapi.json` — spec de API própria antes de codar | 01, 10 | testes da API (status + corpo, isolamento por tenant) | Pendente |
| 9 | Contrato: versionar `openapi.json`, `orval.config.ts`, gerar cliente, adaptar sessão ao contrato gerado | 01 | build; diff do gerado revisado | Pendente; catálogo ainda usa `fetch` manual e schema local |

Specs de funcionalidade ainda necessárias: **002-catalogo** (CA-02, usa rota existente),
**003-solicitar-emprestimo** (CA-03 + 06/07/08), **004-devolucao** (CA-04 + 10),
**005-operacoes** (CA-05), **006-cadastro-equipamento** (CA-09 + form) — cada
uma com spec → plan → tasks, iniciada só após as rotas da API correspondentes
existirem e o `openapi.json` estar atualizado. As telas correspondentes já
existem em modo demonstrativo, mas não substituem essas specs, APIs ou critérios
de aceite.
