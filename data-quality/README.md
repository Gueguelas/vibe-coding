# dq — validador de qualidade de dados

Projeto das aulas 2 e 3 do curso de vibe coding.

Um CLI que recebe um CSV e reporta problemas de qualidade nos dados: valores
faltando, linhas duplicadas e colunas com tipo inconsistente.

## Por que este projeto existe

Todo mundo que trabalha com dados já recebeu uma planilha "pronta" que não
estava pronta. Você carrega, roda a análise, e três horas depois descobre que a
coluna `preco_unitario` tinha `"R$ 1.234,56"` no meio dos números — e que o
relatório que você mandou pro time estava errado desde o começo.

A inspeção manual não escala: você olha as primeiras 20 linhas, elas parecem
boas, e você segue em frente. O arquivo `data/vendas.csv` deste repositório tem
71 linhas e vários problemas plantados de propósito. Alguns são óbvios. Outros
você só encontra se procurar.

O objetivo das duas aulas **não é** escrever esse validador. É usar esse
validador como desculpa para aprender a dar contexto a um agente de IA.

## Setup

Você precisa de Python 3.10+ e do Cursor instalado.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Confirme que funcionou:

```bash
pytest -q                          # deve rodar sem erro (ainda não há testes)
python -c "import pandas; print(pandas.__version__)"
```

## Como isso vai ficar no fim

```bash
dq data/vendas.csv
```

...imprimindo um relatório dos problemas encontrados no terminal.

## Estrutura

```
dq/
├── AGENTS.md              ← você escreve na aula 2
├── .cursor/rules/         ← você escreve na aula 2
├── docs/handoff.md        ← você escreve na aula 3
├── data/vendas.csv        ← já está aqui
├── src/dq/
├── tests/
└── pyproject.toml
```

## Antes da aula

Faça o setup acima e abra a pasta no Cursor. Não escreva código ainda —
o primeiro prompt a gente dá junto, em aula.
