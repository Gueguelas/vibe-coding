# Handoff de fim de sessão

Ao USUÁRIO PEDIR EM UMA SESSÃO:
- gere docs/handoff/handoff-{resumo_basico_da_sessao}.md
SENDO {resumo_basico_da_sessao} - um resumo bem simples do que foi pedido pelo usuário

Com estas seções,
nesta ordem:

## Onde parei
Estado atual em duas ou três frases. O que existe e está funcionando.

## Decisões não óbvias
Só as desta sessão, e só as que ainda não viraram ADR nem regra.
Se já está em docs/adr/ ou no AGENTS.md, aponte — não repita.

## O que tentei e não funcionou
Caminhos descartados, para não serem tentados de novo na próxima sessão.

## Próximo passo exato
Uma ação, com nome de arquivo e de etapa do plano.
Nunca "continuar o projeto".

## Arquivos relevantes
Caminhos, não conteúdo.

Regras de redação:
- Seja específico: nomes de arquivo, de função e de etapa do plano.
- Não repita nada que já esteja no AGENTS.md, em rules/ ou nos ADRs.
- Sobrescreva o arquivo. Não acumule histórico de sessões.