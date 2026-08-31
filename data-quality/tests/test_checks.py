"""Testes do módulo de checks (Etapa 4 do docs/plan.md).

Regras (docs/rules/tests.md):
- pytest puro, sem framework adicional.
- Um cenário por teste.
- Regra de negócio testada SEM banco, com DataFrame montado na mão.
- Datas explícitas e fixas.
"""

import pandas as pd

from src.dq.checks import (
    CHECKS,
    CheckResult,
    check_linhas_duplicadas,
    check_tipo_inconsistente,
    check_valores_faltando,
)


def test_checkresult_ok():
    """CheckResult com nada encontrado tem ok=True e total 0."""
    r = CheckResult(nome="valores_faltando", ok=True, total=0, detalhe="Nada encontrado.")
    assert r.ok is True
    assert r.total == 0
    assert r.nome == "valores_faltando"


def test_checkresult_com_problema():
    """CheckResult com problema tem ok=False e total de ocorrências."""
    r = CheckResult(nome="linhas_duplicadas", ok=False, total=3, detalhe="3 linhas duplicadas.")
    assert r.ok is False
    assert r.total == 3


def test_checkresult_detalhe_sem_quebra():
    """O detalhe não contém quebra de linha."""
    r = CheckResult(nome="tipo_inconsistente", ok=False, total=5, detalhe="5 células com tipo inconsistente.")
    assert "\n" not in r.detalhe
# ---------------------------------------------------------------------------
# check_valores_faltando
# ---------------------------------------------------------------------------


def test_valores_faltando_sem_falta():
    """DataFrame completo retorna ok=True e total 0."""
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    r = check_valores_faltando(df)
    assert r.ok is True
    assert r.total == 0


def test_valores_faltando_conta_nulos_e_vazios():
    """DataFrame com NaN e string vazia retorna ok=False e total 2."""
    df = pd.DataFrame({"a": [1, None], "b": ["x", ""]})
    r = check_valores_faltando(df)
    assert r.ok is False
    assert r.total == 2  # None + "" = 2


def test_valores_faltando_detalhe_tem_colunas():
    """Detalhe lista as colunas com valores faltando."""
    df = pd.DataFrame({"a": [None, None], "b": [1, 2]})
    r = check_valores_faltando(df)
    assert "a" in r.detalhe


# ---------------------------------------------------------------------------
# check_linhas_duplicadas
# ---------------------------------------------------------------------------


def test_linhas_duplicadas_sem_duplicata():
    """DataFrame sem duplicatas retorna ok=True."""
    df = pd.DataFrame({"id_venda": ["V1", "V2"], "a": [1, 2]})
    r = check_linhas_duplicadas(df)
    assert r.ok is True
    assert r.total == 0


def test_linhas_duplicadas_por_id_venda():
    """Duas linhas com mesmo id_venda são detectadas (total=2)."""
    df = pd.DataFrame({"id_venda": ["V1", "V1", "V2"], "a": [1, 5, 3]})
    r = check_linhas_duplicadas(df)
    assert r.ok is False
    assert r.total == 2  # as duas linhas com V1


def test_linhas_duplicadas_por_linha_exata():
    """Linhas exatamente iguais em todas as colunas são detectadas."""
    df = pd.DataFrame({"id_venda": ["V1", "V1"], "a": [1, 1]})
    r = check_linhas_duplicadas(df)
    assert r.ok is False
    assert r.total == 2  # ambas as linhas


def test_linhas_duplicadas_sem_coluna_id_venda():
    """Funciona mesmo sem a coluna id_venda (usa linha exata)."""
    df = pd.DataFrame({"a": [1, 1]})
    r = check_linhas_duplicadas(df)
    assert r.ok is False
    assert r.total == 2


# ---------------------------------------------------------------------------
# check_tipo_inconsistente
# ---------------------------------------------------------------------------


def test_tipo_inconsistente_sem_problema():
    """Colunas numéricas e datas válidas retornam ok=True."""
    df = pd.DataFrame({
        "data_venda": ["2025-01-06", "09/01/2025"],
        "quantidade": [1, 2],
        "preco_unitario": [100.0, 50.5],
    })
    r = check_tipo_inconsistente(df)
    assert r.ok is True
    assert r.total == 0


def test_tipo_inconsistente_preco_formatado_errado():
    """Preço R$ 1.234,56 é detectado como tipo inconsistente."""
    df = pd.DataFrame({
        "preco_unitario": ["R$ 1.234,56", 50.0],
        "quantidade": [1, 2],
        "data_venda": ["2025-01-06", "2025-01-07"],
    })
    r = check_tipo_inconsistente(df)
    assert r.ok is False
    assert r.total == 1  # só "R$ 1.234,56"


def test_tipo_inconsistente_quantidade_por_extenso():
    """Quantidade 'dois' é detectada como tipo inconsistente."""
    df = pd.DataFrame({
        "quantidade": ["dois", 3],
        "preco_unitario": [100.0, 50.0],
        "data_venda": ["2025-01-06", "2025-01-07"],
    })
    r = check_tipo_inconsistente(df)
    assert r.ok is False
    assert r.total == 1


def test_tipo_inconsistente_na_como_preco():
    """"N/A" em preco_unitario é detectado como tipo inconsistente."""
    df = pd.DataFrame({
        "preco_unitario": ["N/A", 100.0],
        "quantidade": [1, 2],
        "data_venda": ["2025-01-06", "2025-01-07"],
    })
    r = check_tipo_inconsistente(df)
    assert r.ok is False
    assert r.total == 1


def test_tipo_inconsistente_nulo_ignorado():
    """NaN em coluna numérica não é erro de tipo (é valores_faltando)."""
    df = pd.DataFrame({
        "preco_unitario": [None, 100.0],
        "quantidade": [1, 2],
        "data_venda": ["2025-01-06", "2025-01-07"],
    })
    r = check_tipo_inconsistente(df)
    assert r.ok is True
    assert r.total == 0


def test_tipo_inconsistente_data_iso_valida():
    """Data ISO é válida para coluna de data."""
    df = pd.DataFrame({
        "data_venda": ["2025-01-06"],
        "quantidade": [1],
        "preco_unitario": [100.0],
    })
    r = check_tipo_inconsistente(df)
    assert r.ok is True


# ---------------------------------------------------------------------------
# CHECKS — dicionário de registros
# ---------------------------------------------------------------------------


def test_checks_contem_tres_chaves():
    """CHECKS tem exatamente as três chaves esperadas."""
    chaves_esperadas = {"valores_faltando", "linhas_duplicadas", "tipo_inconsistente"}
    assert set(CHECKS) == chaves_esperadas


def test_checks_cada_check_retorna_checkresult():
    """Cada função em CHECKS devolve um CheckResult."""
    df = pd.DataFrame({
        "id_venda": ["V1"],
        "a": [1],
        "preco_unitario": [10.0],
        "quantidade": [1],
        "data_venda": ["2025-01-06"],
    })
    for check in CHECKS.values():
        resultado = check(df)
        assert isinstance(resultado, CheckResult)
