# Hermes Skills — Agência

Fonte de skills para o Hermes Agent (via `hermes skills tap add owner/repo`).

Cada pasta é uma skill com seu `SKILL.md`. Departamentos da agência:

## Pesquisa e Estratégia
- `pesquisa-estrategia/` — orquestrador do departamento (fluxo + gates de aprovação)
- `cacador-de-nichos/` — validação de nicho e posicionamento
- `pesquisador-tendencias/` — pesquisa de tendências e oportunidades de conteúdo

## Como usar no Hermes
```
hermes skills tap add SEU_USUARIO/NOME_DO_REPO
hermes skills list
```
As skills ficam disponíveis para o agente. O departamento é acionado pela skill `pesquisa-estrategia`.

> Observação: `pesquisador-tendencias` depende do toolset de web/search habilitado no Hermes.
