"""Tests for the sales analysis module.

Following the project conventions:
- Tests are in tests/ directory
- One test file per module
- Use manually constructed DataFrames
- No dependencies beyond pandas and pytest
"""

import pandas as pd

from src.dq.analisis import (
    _limpar_preco,
    _limpar_quantidade,
    _limpar_data,
    _normalizar_categoria,
    analisar_vendas,
    imprimir_relatorio,
    MetricaVenda,
)


def test_limpar_preco():
    """Testa a limpeza de valores de preço."""
    # Formato R$ 1.234,56
    assert _limpar_preco("R$ 1.234,56") == 1234.56
    # Formato 1.799,00
    assert _limpar_preco("1.799,00") == 1799.0
    # Formato 4899.00
    assert _limpar_preco("4899.00") == 4899.0
    # N/A deve retornar None
    assert _limpar_preco("N/A") is None
    # Vazio deve retornar None
    assert _limpar_preco("") is None
    # None deve retornar None
    assert _limpar_preco(None) is None


def test_limpar_quantidade():
    """Testa a limpeza de valores de quantidade."""
    # Número simples
    assert _limpar_quantidade("3") == 3.0
    # Com vírgula decimal
    assert _limpar_quantidade("3,0") == 3.0
    # Palavra "dois"
    assert _limpar_quantidade("dois") == 2.0
    # Palavra "tres" (com acento)
    assert _limpar_quantidade("três") == 3.0
    # N/A deve retornar None
    assert _limpar_quantidade("N/A") is None
    # Vazio deve retornar None
    assert _limpar_quantidade("") is None


def test_limpar_data():
    """Testa a limpeza de valores de data."""
    # Formato ISO
    assert _limpar_data("2025-01-06") is not None
    assert _limpar_data("2025-01-06").day == 6
    # Formato brasileiro DD/MM/YYYY
    assert _limpar_data("09/01/2025") is not None
    assert _limpar_data("09/01/2025").day == 9
    # N/A deve retornar None
    assert _limpar_data("N/A") is None
    # Vazio deve retornar None
    assert _limpar_data("") is None


def test_normalizar_categoria():
    """Testa a normalização de categorias."""
    # Eletrônicos
    assert _normalizar_categoria("eletrônicos") == "Eletrônicos"
    assert _normalizar_categoria("ELETRÔNICOS") == "Eletrônicos"
    assert _normalizar_categoria("Eletrônicos") == "Eletrônicos"
    # Móveis
    assert _normalizar_categoria("Móveis") == "Móveis"
    assert _normalizar_categoria("moveis") == "Móveis"
    assert _normalizar_categoria("MOVEIS") == "Móveis"
    # Categoria desconhecida deve retornar None
    assert _normalizar_categoria("Alimentos") is None
    # Vazio deve retornar None
    assert _normalizar_categoria("") is None


def test_metrica_venda_dataclass():
    """Testa que MetricaVenda é um dataclass válido."""
    m = MetricaVenda(nome="Test", total=100.0, detalhe="teste")
    assert m.nome == "Test"
    assert m.total == 100.0
    assert m.detalhe == "teste"


def test_analisar_vendas_vazio():
    """Testa análise com DataFrame vazio."""
    resultado = analisar_vendas(pd.DataFrame())
    assert resultado == []


def test_imprimir_relatorio():
    """Testa a impressão de relatório."""
    metricas = [
        MetricaVenda(nome="Receita total", total=130323.76, detalhe="66 vendas"),
    ]
    # Só verifica se não dá erro (saída vai para stdout)
    imprimir_relatorio(metricas)


def test_analisar_vendas_completo():
    """Testa análise completa com DataFrame construído manualmente."""
    df = pd.DataFrame({
        "id_venda": ["V001", "V002", "V003"],
        "data_venda": ["2025-01-15", "2025-01-20", "2025-02-10"],
        "cliente": ["Maria", "João", "Pedro"],
        "produto": ["Notebook", "Mouse", "Teclado"],
        "categoria": ["Eletrônicos", "Eletrônicos", "Acessórios"],
        "quantidade": [1, 2, 1],
        "preco_unitario": [1000.0, 50.0, 100.0],
        "regiao": ["Sudeste", "Sul", "Nordeste"],
        "vendedor": ["Ana", "Bruno", "Carla"],
    })

    # Aplicar limpezas
    df["preco_unitario"] = df["preco_unitario"].apply(lambda x: _limpar_preco(x))
    df["quantidade"] = df["quantidade"].apply(lambda x: _limpar_quantidade(x))
    df["data_venda"] = df["data_venda"].apply(lambda x: _limpar_data(x))
    df["categoria"] = df["categoria"].apply(lambda x: _normalizar_categoria(x))

    # Linhas com dados essenciais None são removidas
    df = df.dropna(subset=["preco_unitario", "quantidade", "data_venda"])

    resultado = analisar_vendas(df)

    # Deve ter métricas
    assert len(resultado) > 0
    # Deve ter receita total
    receita_total = next((m for m in resultado if m.nome == "Receita total"), None)
    assert receita_total is not None
    assert receita_total.total == 1200.0  # 1000 + 50*2 + 100 = 1200
    assert "3 vendas" in receita_total.detalhe