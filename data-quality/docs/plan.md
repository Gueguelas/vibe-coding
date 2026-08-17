# Plano de implementação — dq (validador de qualidade de dados)

> Documento vivo. Este plano divide o trabalho em etapas pequenas, cada uma com
> uma validação de "pronto" para ser executada antes de avançar (ver
> `docs/rules/checks.md`). Decisões de arquitetura que já existem não são
> repetidas aqui — veja `AGENTS.md`, `docs/rules/*` e `docs/adr/*`.

## Objetivo

Transformar o código atual no validador de qualidade de dados descrito em
`AGENTS.md` e no `README.md`: um CLI `dq data/vendas.csv` que lê um CSV e
reporta problemas de qualidade (valores faltando, linhas duplicadas, tipos
inconsistentes). O CLI **não corrige nada e não escreve arquivo** — só lê e
relata para o stdout.

### Estado atual (baseline)

- `pyproject.toml` já expõe o entry point `dq = "dq.cli:main"`, mas **não existe
  `src/dq/cli.py`**.
- `AGENTS.md` e `rules/checks.mdc` definem a arquitetura-alvo: `cli.py`
  (argumentos/impressão), `checks.py` (validações), dataclass `CheckResult`,
  dicionário `CHECKS`.
- Existe `src/dq/analisis.py` + `tests/test_analisis.py` (módulo de "análise de
  vendas"). É uma **divergência** com a arquitetura-alvo. 8 testes passam.
- `data/vendas.csv` (somente leitura) tem 71 linhas com problemas plantados.

---

## Etapa 0 — Alinhar nomenclatura e decidir o destino do `analisis.py`

### O que fazer
1. Confirmar a arquitetura-alvo em `AGENTS.md` (estrutura `cli.py` + `checks.py`).
2. Decidir o destino de `src/dq/analisis.py` e `tests/test_analisis.py`:
   - **Recomendação:** remover os dois arquivos (restos de uma direção
     anterior) para não conflitar com `checks.py`, preservando o histórico no
     git. Só remover com autorização explícita.
3. Garantir `src/dq/__init__.py` existente e vazio (sem lógica).

### Definição de pronto (validação)
- `pytest -q` continua passando (ou a suíte anterior foi migrada de forma
  consciente).
- A estrutura bate com `AGENTS.md`.

---

## Etapa 1 — Dataclass `CheckResult` em `src/dq/checks.py`

### O que fazer
1. Criar `src/dq/checks.py` com a dataclass `CheckResult`:
   - campos `nome`, `ok`, `total`, `detalhe`;
   - `ok` é `True` quando NADA foi encontrado;
   - `total` é o número de ocorrências (não de linhas);
   - `detalhe` é frase curta em português, sem quebra de linha
     (regras de `rules/checks.mdc`).

### Definição de pronto (validação)
- Teste unitário mínimo do `CheckResult` (construído à mão) antes dos checks
  existirem.

---

## Etapa 2 — Implementar os checks em `src/dq/checks.py`

Cada check segue a assinatura `def check_<nome>(df: pd.DataFrame) -> CheckResult`
(só `df`, sem parâmetro extra), e todos são registrados no dicionário `CHECKS`
no fim do arquivo.

### O que fazer
1. `check_valores_faltando` — por coluna, conta nulos/vazios; `ok=True`
   quando nada falta.
2. `check_linhas_duplicadas` — detecta duplicatas de `id_venda` e duplicatas
   exatas de linha; `total` = nº de linhas duplicadas.
3. `check_tipo_inconsistente` — colunas que deveriam ser numéricas/datas com
   valores que não convertem (ex.: `"R$ 1.234,56"`, `"dois"`, `"N/A"`);
   `total` = nº de células problemáticas.
4. Registrar todos no dicionário `CHECKS` (nunca `if/elif`).
5. Não usar `print` dentro de `checks.py` — quem imprime é o `cli.py`.

### Definição de pronto (validação)
- Testes de cada `check_*` com DataFrames montados na mão (ver Etapa 4).

---

## Etapa 3 — `src/dq/cli.py` (argumentos + impressão)

### O que fazer
1. `argparse` com `caminho_csv` posicional → comportamento `dq data/vendas.csv`
   (entry point já declarado no `pyproject.toml`).
2. Ler o CSV com `pandas`.
3. Importar e iterar sobre o dicionário `CHECKS` — o `cli.py` **não conhece
   checks pelo nome** e não contém regra de negócio.
4. Imprimir cada `CheckResult` no stdout (formato legível com `ok`/falha e
   `detalhe`).
5. Não escrever arquivo de relatório.

### Definição de pronto (validação)
- `python -m dq.cli data/vendas.csv` roda e reporta os problemas esperados no CSV.
- `dq data/vendas.csv` funciona após instalação (`pip install -e ".[dev]"`).

---

## Etapa 4 — Testes (`tests/test_checks.py`)

### O que fazer
1. Seguir `docs/rules/tests.md`: pytest puro, um cenário por teste, datas
   explícitas, regra de negócio testada sem banco.
2. Cobertura: `CheckResult`, cada `check_*` (caso ok e caso com problema) e
   iteração sobre `CHECKS`.

### Definição de pronto (validação)
- `pytest -q` todo verde, sem regressão.

---

## Etapa 5 — Integração e "definição de pronto" final

### O que fazer
1. Seguir `docs/rules/checks.md`:
   - rodar a suíte completa;
   - validar a validação da etapa atual;
   - confirmar que nenhum teste anterior regrediu;
   - confirmar que os ADRs são respeitados (sem banco/IO no domínio; a única
     leitura é do CSV pelo CLI).
2. Atualizar `README.md` se necessário para refletir o comportamento real.
3. Se pedido, gerar `docs/handoff.md` no formato de `docs/rules/handoff.md`.

### Definição de pronto (validação)
- `pytest -q` verde.
- `dq data/vendas.csv` gera relatório correto no stdout.
- `data/` não foi modificado.

---

## Riscos e pontos de atenção

- **`analisis.py` vs `checks.py`**: evitar duas frentes de código semânticas
  diferentes; a Etapa 0 resolve.
- **Não adicionar dependências**: apenas `pandas` e `pytest` (ver `O que NÃO
  fazer` no `AGENTS.md`).
- **`data/` é somente leitura**: o CLI nunca grava nem modifica `data/`.
- **ADR-001/002/003** referem-se a outro sistema (Programa de Pontos); manter a
  separação de fronteiras de qualquer forma.