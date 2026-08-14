"""Análise de vendas a partir de um CSV de vendas.

Este módulo lê um CSV de vendas, limpa os dados problemáticos
e calcula métricas de negócio: receita total, vendas por região,
por produto, por categoria, por vendedor, tendência mensal, etc.

Convencões do projeto:
- Apenas pandas como dependência.
- Não escreve arquivos: a saída vai para stdout (quem imprime é o CLI).
- Não toca data/ (somente leitura).
"""

from __future__ import annotations

import dataclasses
import re

import pandas as pd


# ---------------------------------------------------------------------------
# Limpeza de dados
# ---------------------------------------------------------------------------


def _limpar_preco(valor) -> float | None:
    """Converte um valor de preço para float numérico.

    Maneja formatos como "R$ 1.234,56", "1.799,00", "4899.00", "N/A", "".
    Retorna None se não for possível converter.
    """
    if valor is None:
        return None
    texto = str(valor).strip()
    if not texto or texto.upper() in {"N/A", "NA", "NAN", "NULL", "NONE"}:
        return None
    # Remover símbolo de moeda e espaços
    texto = texto.replace("R$", "").replace("$", "").strip()
    # Detectar formato europeu: "1.234,56" ou "1.799,00"
    if re.match(r"^\d{1,3}(\.\d{3})+(,\d+)?$", texto):
        texto = texto.replace(".", "").replace(",", ".")
    # Detectar formato com vírgula decimal simples: "1234,56"
    elif re.match(r"^\d+(,\d+)?$", texto) and "," in texto:
        texto = texto.replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def _limpar_quantidade(valor) -> float | None:
    """Converte um valor de quantidade para numérico.

    Maneja "3", "3,0", "dois", "três", "N/A", "".
    Retorna None se não for possível converter.
    """
    if valor is None:
        return None
    texto = str(valor).strip()
    if not texto or texto.upper() in {"N/A", "NA", "NAN", "NULL", "NONE"}:
        return None
    # Palavras numéricas em português
    palavras = {
        "zero": 0,
        "um": 1,
        "uma": 1,
        "dois": 2,
        "duas": 2,
        "tres": 3,
        "três": 3,
        "quatro": 4,
        "cinco": 5,
        "seis": 6,
        "sete": 7,
        "oito": 8,
        "nove": 9,
        "dez": 10,
    }
    if texto.lower() in palavras:
        return float(palavras[texto.lower()])
    # Formato com vírgula decimal: "3,0"
    if re.match(r"^\d+(,\d+)?$", texto) and "," in texto:
        texto = texto.replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def _limpar_data(valor) -> pd.Timestamp | None:
    """Converte um valor de data para datetime.

    Maneja "2025-01-06" e "09/01/2025".
    Retorna None se não for possível converter.
    """
    if valor is None:
        return None
    texto = str(valor).strip()
    if not texto or texto.upper() in {"N/A", "NA", "NAN", "NULL", "NONE"}:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return pd.to_datetime(texto, format=fmt)
        except ValueError:
            continue
    try:
        return pd.to_datetime(texto)
    except (ValueError, TypeError):
        return None


def _normalizar_categoria(valor) -> str | None:
    """Normaliza variantes de categoria para um valor canônico.

    "eletrônicos", "ELETRÔNICOS", "Eletrônicos" -> "Eletrônicos"
    "Móveis", "moveis", "MOVEIS" -> "Móveis"
    Retorna None se não for possível normalizar.
    """
    if valor is None:
        return None
    texto = str(valor).strip()
    if not texto:
        return None
    # Mapeamento de variantes para categoria canônica (chaves em minúsculo para lookup case-insensitive)
    mapa_lower = {
        "eletrônicos": "Eletrônicos",
        "eletronicos": "Eletrônicos",
        "móveis": "Móveis",
        "moveis": "Móveis",
    }
    # Tenta lookup direto com minúsculas
    resultado = mapa_lower.get(texto.lower())
    if resultado:
        return resultado
    # Fallback: tenta match exato ignorando maiúsculas
    texto_lower = texto.lower()
    for chave, valor in mapa_lower.items():
        if chave == texto_lower:
            return valor
    return None


# ---------------------------------------------------------------------------
# Análise e métricas
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class MetricaVenda:
    """Resultado de uma métrica de análise de vendas."""
    nome: str
    total: float
    detalhe: str


def analisar_vendas(df: pd.DataFrame) -> list[MetricaVenda]:
    """Analisa um DataFrame de vendas limpo e retorna métricas.

    Args:
        df: DataFrame com colunas de vendas já limpas.

    Retorna:
        Lista de MetricaVenda com os resultados da análise.
    """
    if df.empty:
        return []

    # Garantir tipos corretos
    df = df.copy()

    # Calcular receita da venda individual
    df["receita"] = df["quantidade"] * df["preco_unitario"]

    metricas = []

    # Receita total
    receita_total = df["receita"].sum()
    metricas.append(
        MetricaVenda(
            nome="Receita total",
            total=receita_total,
            detalhe=f"{len(df)} vendas",
        )
    )

    # Vendas por região
    por_regiao = df.groupby("regiao")["receita"].agg(["sum", "count"]).reset_index()
    for _, linha in por_regiao.iterrows():
        metricas.append(
            MetricaVenda(
                nome=f"Receita por região - {linha['regiao']}",
                total=linha["sum"],
                detalhe=f"{int(linha['count'])} vendas",
            )
        )

    # Vendas por produto (top 5 por receita)
    por_produto = (
        df.groupby("produto")["receita"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    for produto, total in por_produto.items():
        metricas.append(
            MetricaVenda(
                nome=f"Produto - {produto}",
                total=total,
                detalhe=f"{df[df['produto'] == produto].shape[0]} vendas",
            )
        )

    # Vendas por categoria
    por_categoria = (
        df.groupby("categoria")["receita"]
        .sum()
        .sort_values(ascending=False)
    )
    for categoria, total in por_categoria.items():
        metricas.append(
            MetricaVenda(
                nome=f"Categoria - {categoria}",
                total=total,
                detalhe=f"{df[df['categoria'] == categoria].shape[0]} vendas",
            )
        )

    # Ticket médio
    ticket_medio = receita_total / len(df) if len(df) > 0 else 0
    metricas.append(
        MetricaVenda(
            nome="Ticket médio",
            total=ticket_medio,
            detalhe=f"Receita / {len(df)} vendas",
        )
    )

    # Tendência mensual
    df_mes = (
        df.copy()
        .assign(mes=df["data_venda"].dt.to_period("M"))
        .groupby("mes")["receita"]
        .sum()
        .sort_index()
    )
    for mes, total in df_mes.items():
        metricas.append(
            MetricaVenda(
                nome=f"Mês {mes}",
                total=total,
                detalhe=f"{df[df['data_venda'].dt.to_period('M') == mes].shape[0]} vendas",
            )
        )

    return metricas


# ---------------------------------------------------------------------------
# Utilitário para imprimir relatório
# ---------------------------------------------------------------------------


def imprimir_relatorio(metricas: list[MetricaVenda]) -> None:
    """Imprime um relatório de métricas de vendas no stdout.

    Args:
        metricas: Lista de MetricaVenda gerada por analisar_vendas().
    """
    if not metricas:
        print("Nenhuma métrica encontrada.")
        return

    print("=== ANÁLISE DE VENDAS ===")
    for m in metricas:
        # Formatar total em moeda brasileira
        total_formatado = f"R$ {m.total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f"{m.nome}: {total_formatado} - {m.detalhe}")
    print("=== FIM ===")


# ---------------------------------------------------------------------------
# Função principal para usar como script
# ---------------------------------------------------------------------------


def main(caminho_csv: str) -> None:
    """Função principal: lê CSV, limpa e imprime relatório de análise.

    Args:
        caminho_csv: Caminho para o arquivo CSV de vendas.
    """
    # Ler CSV
    df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

    # Limpar e normalizar colunas
    # - preco_unitario
    df["preco_unitario"] = df["preco_unitario"].apply(_limpar_preco)
    # - quantidade
    df["quantidade"] = df["quantidade"].apply(_limpar_quantidade)
    # - data_venda
    df["data_venda"] = df["data_venda"].apply(_limpar_data)
    # - categoria
    df["categoria"] = df["categoria"].apply(_normalizar_categoria)

    # Remover linhas onde dados essenciais são None
    df = df.dropna(subset=["preco_unitario", "quantidade", "data_venda"])

    # Analisar
    metricas = analisar_vendas(df)

    # Imprimir relatório
    imprimir_relatorio(metricas)