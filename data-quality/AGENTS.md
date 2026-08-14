# AGENTS.md

## O que é este projeto
`dq` é um CLI que lê um CSV e reporta problemas de
qualidade nos dados. Não corrige nada, não escreve
arquivos — só lê e relata.

## Comandos
pytest -q                 # roda os testes
dq data/vendas.csv        # roda o CLI

## Estrutura
src/dq/cli.py      → argumentos e impressão. Sem regra de negócio.
src/dq/checks.py   → todas as validações.
tests/             → um arquivo de teste por módulo.
data/              → somente leitura, nunca sobrescrever.

## Convenções obrigatórias
- Todo check devolve um `CheckResult` (dataclass com
  nome, ok, total, detalhe). Nunca `bool`, nunca string solta.
- Checks são registrados no dicionário `CHECKS`, nunca em if/elif.
- Toda função de check recebe `df: pd.DataFrame` e devolve
  `CheckResult`. Sem parâmetros posicionais extras.
- A saída vai para stdout. Não escreva arquivo de relatório.
- Nada de `print` dentro de `checks.py`. Quem imprime é o `cli.py`.

## O que NÃO fazer
- Não adicione dependências. `pandas` e `pytest` bastam.
- Não crie `utils.py`, `helpers.py` ou `common.py`.
- Não escreva nem modifique nada em `data/`.
- Não refatore código fora do pedido atual.