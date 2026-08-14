# handoff.md

## Resumo da Implementação

Este documento descreve o que foi implementado nas aulas 2 e 3 do curso de vibe coding.

### O que foi criado

1. **`src/dq/analisis.py`** - Módulo de análise de vendas:
   - Funções de limpeza de dados (`_limpar_preco`, `_limpar_quantidade`, `_limpar_data`, `_normalizar_categoria`)
   - Função de análise (`analisar_vendas`) que calcula métricas de negócio
   - Função de relatório (`imprimir_relatorio`) que imprime no stdout
   - Função principal (`main`) que orquestra o processo
   - Dataclass `MetricaVenda` para estruturar os resultados

2. **`tests/test_analisis.py`** - 8 testes unitários:
   - test_limpar_preco, test_limpar_quantidade, test_limpar_data
   - test_normalizar_categoria, test_metrica_venda_dataclass
   - test_analisar_vendas_vazio, test_imprimir_relatorio
   - test_analisar_vendas_completo

3. **`docs/handoff.md`** - Este documento

### Como usar

```bash
# Instalar dependências
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Rodar os testes
pytest -q

# Rodar a análise de vendas
python -m src.dq.analisis main data/vendas.csv
```

### Problemas tratados

O módulo lida com os seguintes problemas de qualidade de dados encontrados em `data/vendas.csv`:

- Valores faltando em colunas como `cliente`, `quantidade`, `preco_unitario`, `categoria`
- Tipos inconsistentes: `"R$ 1.234,56"` na coluna `preco_unitario`, `"dois"` na coluna `quantidade`
- Formatos de data mistos: `"2025-01-06"` e `"09/01/2025"`
- Categorias variantes: `"eletrônicos"`, `"ELETRÔNICOS"`, `"Móveis"`, `"moveis"`

### Métricas calculadas

- Receita total
- Receita por região
- Receita por produto (top 5)
- Receita por categoria
- Ticket médio
- Tendência mensal

### Testes

Todos os 8 testes passam (`pytest -q` → 8 passed), cobrindo:
- Limpeza de preços (formatos R$, numéricos, N/A, vazios)
- Limpeza de quantidades (números, palavras em português, vírgula decimal)
- Limpeza de datas (formato ISO e brasileiro)
- Normalização de categorias
- Dataclass MetricaVenda
- Análise com DataFrame vazio
- Impressão de relatório
- Análise completa com dados de teste