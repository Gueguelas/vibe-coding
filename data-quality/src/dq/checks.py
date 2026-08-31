"""Checks de qualidade de dados.

Cada check devolve um ``CheckResult`` (nunca ``bool``, nunca string solta).
Nesta etapa o módulo contém apenas a dataclass `CheckResult`; as funções
``check_*`` e o dicionário ``CHECKS`` são adicionados nas etapas seguintes,
conforme o ``docs/plan.md``.

Convenções (ver ``AGENTS.md`` e ``rules/checks.mdc``):
- Assinatura: ``def check_<nome>(df: pd.DataFrame) -> CheckResult``
- ``ok`` é ``True`` quando NADA foi encontrado.
- ``total`` é o número de ocorrências, não de linhas.
- ``detalhe`` é frase curta em português sem quebra de linha.
- Quem imprime é o ``cli.py`` — nenhum ``print`` aqui.
- Todos os checks são registrados no dicionário ``CHECKS`` (nunca ``if/elif``).
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class CheckResult:
    """Resultado de um check de qualidade de dados.

    Attributes:
        nome: Nome do check, usado para identificar o resultado no relatório.
        ok: True quando NADA foi encontrado; False quando há problema.
        total: Número de ocorrências do problema (não de linhas).
        detalhe: Frase curta em português, sem quebra de linha.
    """

    nome: str
    ok: bool
    total: int
    detalhe: str


# ---------------------------------------------------------------------------
# Funções auxiliares internas (não expostas no dicionário CHECKS)
# ---------------------------------------------------------------------------


def _esta_faltando(valor) -> bool:
    """True se o valor é nulo, NaN ou string vazia/só-espaços."""
    if pd.isna(valor):
        return True
    if isinstance(valor, str) and valor.strip() == "":
        return True
    return False


def _eh_numerico(valor) -> bool:
    """True se o valor é NaN, numérico, ou string com float Python válido."""
    if pd.isna(valor):
        return True  # não é erro de tipo
    if isinstance(valor, (int, float)):
        return True
    texto = str(valor).strip()
    if not texto:
        return True  # vazio → valores_faltando pega
    try:
        float(texto)
        return True
    except ValueError:
        return False


def _eh_data(valor) -> bool:
    """True se o valor é NaN, Timestamp, ou string de data válida."""
    if pd.isna(valor):
        return True
    if isinstance(valor, pd.Timestamp):
        return True
    texto = str(valor).strip()
    if not texto:
        return True
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            pd.to_datetime(texto, format=fmt)
            return True
        except (ValueError, TypeError):
            continue
    # fallback tenta padrão do pandas
    try:
        pd.to_datetime(texto)
        return True
    except (ValueError, TypeError):
        return False


# Colunas do CSV que devem ser numéricas (para verificação de tipo)
_COLUNAS_NUMERICAS = {"quantidade", "preco_unitario"}
# Colunas do CSV que devem ser datas
_COLUNAS_DATA = {"data_venda"}

# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def check_valores_faltando(df: pd.DataFrame) -> CheckResult:
    """Conta valores nulos/vazios em cada coluna do DataFrame.

    Returns:
        CheckResult com ok=True quando nada falta.
    """
    colunas_problema: dict[str, int] = {}
    total = 0
    for col in df.columns:
        n = int(df[col].apply(_esta_faltando).sum())
        if n:
            colunas_problema[col] = n
            total += n

    ok = total == 0
    if ok:
        detalhe = "Nenhum valor faltando."
    else:
        parte = ", ".join(f"{col}: {n}" for col, n in colunas_problema.items())
        detalhe = f"{total} valores faltando ({parte})."
    return CheckResult(nome="Valores faltando", ok=ok, total=total, detalhe=detalhe)


def check_linhas_duplicadas(df: pd.DataFrame) -> CheckResult:
    """Detecta linhas duplicadas por id_venda e/ou linha exata.

    Returns:
        CheckResult com total = nº de linhas que participam de alguma
        duplicação (união das duas detecções).
    """
    duplicadas = pd.Series(False, index=df.index)

    if "id_venda" in df.columns:
        duplicadas |= df["id_venda"].duplicated(keep=False)
    duplicadas |= df.duplicated(keep=False)

    total = int(duplicadas.sum())
    ok = total == 0
    if ok:
        detalhe = "Nenhuma linha duplicada."
    else:
        detalhe = f"{total} linhas duplicadas (por id_venda ou linha exata)."
    return CheckResult(nome="Linhas duplicadas", ok=ok, total=total, detalhe=detalhe)


def check_tipo_inconsistente(df: pd.DataFrame) -> CheckResult:
    """Verifica células que não convertem para o tipo esperado da coluna.

    Colunas numéricas esperadas: ``quantidade``, ``preco_unitario``.
    Coluna de data esperada: ``data_venda``.
    Valores nulos/vazios são ignorados (são capturados por
    ``check_valores_faltando``).

    Returns:
        CheckResult com total = nº de células problemáticas.
    """
    celulas: dict[str, int] = {}
    total = 0

    for col in _COLUNAS_NUMERICAS:
        if col not in df.columns:
            continue
        mask = ~df[col].apply(_eh_numerico)
        n = int(mask.sum())
        if n:
            celulas[col] = n
            total += n

    for col in _COLUNAS_DATA:
        if col not in df.columns:
            continue
        mask = ~df[col].apply(_eh_data)
        n = int(mask.sum())
        if n:
            celulas[col] = n
            total += n

    ok = total == 0
    if ok:
        detalhe = "Nenhuma célula com tipo inconsistente."
    else:
        parte = ", ".join(f"{col}: {n}" for col, n in celulas.items())
        detalhe = f"{total} células com tipo inconsistente ({parte})."
    return CheckResult(nome="Tipo inconsistente", ok=ok, total=total, detalhe=detalhe)


# ---------------------------------------------------------------------------
# Registro no dicionário CHECKS (nunca if/elif)
# ---------------------------------------------------------------------------

CHECKS: dict[str, callable] = {
    "valores_faltando": check_valores_faltando,
    "linhas_duplicadas": check_linhas_duplicadas,
    "tipo_inconsistente": check_tipo_inconsistente,
}

