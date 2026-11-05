# Spec — 001-fundacao-front

- Status: **fundação parcialmente implementada**. Esta spec registra o alvo
  arquitetural; o estado real e as diferenças estão descritos abaixo e no
  `plan.md`/`tasks.md`.
- Perguntas de produto: respostas assumidas por decisão do operador
  ("assuma o que achar melhor e prossiga", 19/10/2026), sem alterar os ADRs.
- plan.md e tasks.md: escritos a partir desta spec

## Contexto

O front já existe em `frontend/`; esta spec foi escrita antes de sua
implementação. A stack alvo está decidida no ADR-001 (React + Vite + React
Router data APIs + TanStack Query + Zustand + RHF/zodResolver + Tailwind +
shadcn/ui + cliente orval + supabase-js) e o visual no ADR-002 (Nocturne dark,
acento teal `#2fb8ac` como linha, Raleway, Phosphor, 5 telas + modal/toast). O
protótipo aprovado está em `prototipo/catalogo.html`.

Esta spec cobre a **fundação** do front inteiro (scaffold, design system,
roteamento, sessão, camada de API, shell de navegação, modal/toast, módulo de
regras derivadas, setup de testes). As telas viram specs próprias (catálogo,
solicitar/devolver, Operações, cadastro) seguindo o mesmo fluxo.

## Estado da implementação (05/11/2026)

- Existem scaffold, rotas, shell, login, catálogo, telas de empréstimos e
  Operações, cadastro, componentes visuais e testes em `frontend/`.
- Login usa Supabase Auth quando configurado; sem configuração, existe uma
  sessão de demonstração e o atalho de Operações fica disponível. O token
  demonstrativo não autentica na API.
- Catálogo consulta `GET /v1/equipamentos` com um cliente `fetch` provisório e
  validação Zod. O OpenAPI não é publicado e o cliente Orval não foi gerado.
- Papel é extraído das claims do JWT no front; `GET /v1/sessao` não existe.
  Isso diverge do fluxo de autorização definido nesta spec e no ADR-001.
- Solicitações, devoluções, painel de Operações e cadastro usam fixtures ou
  estado em memória; não são operações persistidas pela API.
- Os testes E2E atuais cobrem login de demonstração e leitura/falha do
  catálogo, não os fluxos completos de empréstimo e devolução.
- As telas foram implementadas sem as specs próprias previstas abaixo. Não
  tratar a existência visual das telas como critério de aceite dos itens do
  PRD.

## Escopo proposto

1. Scaffold Vite + React + TypeScript `strict` em `frontend/`.
2. Design system do ADR-002 implementado como tokens Tailwind + variantes
   shadcn/ui (botão primário em contorno, pills, escala tipográfica Raleway,
   medidas da seção 4 do ADR-002).
3. React Router (data APIs): rotas com `loader` de sessão, shell com barra de
   navegação por papel (ADR-002 §7).
4. Sessão via `supabase-js` (ADR-001 §7): token no header `Authorization`,
   guard de rota e guard de papel.
5. Camada de API: `openapi.json` versionado + orval gerando
   `src/api/generated` (nunca editar à mão); TanStack Query com invalidação e
   polling.
6. Modal de confirmação e toast conforme ADR-002 §6.6 (420px; toast 2600ms).
7. Módulo de regras derivadas puro (`src/regras/`) — situação, limite de 3,
   bloqueio por atraso, KPIs, prazo 14 dias, `DD/MM/AAAA` — com testes Vitest.
8. Playwright com os fluxos críticos: login, solicitar empréstimo, devolver
   (ADR-001 §8).

## Fora de escopo

- Reserva com data futura, notificação por e-mail, importação de planilha (PRD).
- Tela de convite/provisionamento (o PRD não cobre).
- Tema claro, animações além das do ADR-002 §9.
- Deploy, config da Vercel, variáveis de ambiente reais (proibido para o agente).

## Perguntas que o PRD e os ADRs não respondem — e as respostas assumidas

1. **Origem do papel do usuário na UI — decisão desta spec: endpoint
   `GET /v1/sessao` na API**, retornando `nome`, `email` e `papel`
   (`memberships` do tenant do JWT). O front atual extrai o papel das claims
   do JWT e a API não tem essa rota; isso é uma divergência provisória, não uma
   alteração aprovada do ADR-001. A rota e os guards integrados continuam
   pendentes.
2. **Ordem API × front — decisão desta spec: contrato primeiro; a API cumpre
   antes de cada tela integrada.** A implementação atual adiantou telas e
   mocks antes dos endpoints correspondentes. Não confundir esses mocks com
   integração pronta nem com contrato da API.
3. **Repositório — ASSUMIDO: o front nasce em `frontend/` desta cópia**, na
   mesma situação da API (`backend/`), com migração para repositório próprio
   como pendência já registrada no AGENTS.md (não muda o ADR-001).
4. **Botão "Entrar como Operações" — decisão desta spec: não existe em
   produção.** O código atual exibe o atalho apenas no modo de demonstração,
   sem Supabase configurado; isso é conveniência local e não concede acesso
   real à API.
5. **Responsividade abaixo de 1360px — ASSUMIDO: desktop-first, largura mínima
   suportada 1024px** (colunas quebram por `auto-fill`/grid natural, sem
   design de tablet/mobile na v1). Abaixo de 1024px não há compromisso.
6. **Acessibilidade além do contraste — ASSUMIDO: semântica e foco pelos
   primitivos (botão/label/inputs nativos por trás do shadcn) + regra de foco do
   ADR-002 §5; sem auditoria WCAG dedicada na v1.** Reavaliar antes da entrega
   final.
7. **Paginação do catálogo — usar o cursor retornado pela API, sem paginação
   por offset.** O código atual busca até 20 páginas e acumula os resultados;
   o botão "Carregar mais" descrito inicialmente não foi implementado. A
   decisão de interação ainda precisa ser fechada em uma spec de catálogo.

## Requisitos do PRD mapeados por esta spec e as seguintes

- Item 1 (Login + escopo por pessoa) · Item 2 (catálogo) · Item 3 (solicitar)
  · Item 4 (devolver) · Item 5 (tela de Operações) · regras: limite 3,
  prazo 14 dias, atraso bloqueia, manutenção nunca disponível. O mapeamento
  não significa que os critérios estejam completos ou aceitos; ver o estado
  de implementação acima e os checks de `tasks.md`.
