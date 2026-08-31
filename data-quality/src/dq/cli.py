"""CLI do dq: lê um CSV e reporta problemas de qualidade no stdout.

Regras (ver ``AGENTS.md``):
- A única leitura de I/O é a do CSV, feita aqui.
- Não escreve arquivo de relatório; a saída vai para o stdout.
- Não conhece os checks pelo nome — itera sobre ``CHECKS``.
- ``cli.py`` não contém regra de negócio.
"""

from __future__ import annotations

import argparse
import sys

import pandas as pd

from dq.checks import CHECKS


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dq",
        description="Valida a qualidade dos dados de um CSV e reporta os problemas no stdout.",
    )
    parser.add_argument("caminho_csv", help="Caminho para o arquivo CSV de vendas.")
    args = parser.parse_args(argv)

    df = pd.read_csv(args.caminho_csv)

    resultados = [check(df) for check in CHECKS.values()]

    print(f"Arquivo: {args.caminho_csv}\n")
    for resultado in resultados:
        status = "OK" if resultado.ok else "FALHA"
        print(f"[{status}] {resultado.nome} ({resultado.total})")
        print(f"        {resultado.detalhe}")

    falhas = [r for r in resultados if not r.ok]
    if falhas:
        print(f"\n{len(falhas)} check(s) com problemas.")
        return 1
    print("\nNenhum problema encontrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())