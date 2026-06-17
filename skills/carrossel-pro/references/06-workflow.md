# 06 — WORKFLOW OPERACIONAL
## Manual rápido das fases, checklists e erros comuns

---

## Tempo por fase

| Fase | Nome | 1ª vez | Próximos |
|---|---|---|---|
| 0 | Boas-vindas | 1 min | — |
| 1 | Descoberta de marca | 10-15 | — (`@reusar`) |
| 2 | Sistema visual | 8-12 | — (`@reusar`) |
| 3 | Voz | 5-8 | — (`@reusar`) |
| 4 | Briefing | 3-5 | 3-5 |
| 5 | Big Idea | 5 | 5 |
| 6 | Estrutura | 5 | 5 |
| 7 | Copy | 10-15 | 10-15 |
| 8 | HTML + render | 5-10 | 5-10 |
| 9 | Legenda + entrega | 5 | 5 |
| | **Total** | **~50-70 min** | **~30-40 min** |

No `@express`, junte Fases 1-4 numa rodada de 3-4 perguntas e caia direto na 5-8.

---

## Checklist antes de renderizar (Fase 8)

- [ ] Capa tem promessa clara que para o scroll?
- [ ] 1 ideia por slide, corpo curto (máx. 3 linhas)?
- [ ] Tem 1 slide `breather` se o carrossel tem 8+?
- [ ] Último slide tem CTA único?
- [ ] `kit` e `paleta` batem com o sistema visual definido?
- [ ] `handle` preenchido?
- [ ] Voz aplicada (formalidade, gírias, emojis, lista negra respeitada)?

## Checklist antes de entregar (Fase 9)

- [ ] PNGs revisados (sem texto cortado, contraste ok)?
- [ ] Legenda na voz da marca, com gancho na 1ª linha?
- [ ] Hashtags (5-12) relevantes?
- [ ] Sistema visual salvo pro usuário reutilizar?

---

## Erros comuns (evite)

- **Produzir sem descoberta.** Pular Fases 1-3 no modo completo gera carrossel genérico. Não faça.
- **Impor um tom padrão.** Não use um tom só porque é "seu" jeito — use a voz que a marca da pessoa pede. Coaching executivo formal ≠ marca jovem de games.
- **Acento em tudo.** Se a cor de acento está em todo elemento, ela perde o impacto. Use em kicker, régua, número e CTA.
- **Capa cheia.** Capa com 5 linhas de texto não para scroll. Promessa curta + respiro.
- **Misturar fontes de kits diferentes** sem motivo. Quebra a consistência.
- **Texto centralizado.** O sistema é left-aligned de propósito (leitura). Não centralize.
- **Esquecer de validar.** Cada `[VALIDAR]` é um ponto de confirmação. Você é co-criador.
- **Render sem Playwright e não avisar.** Se não dá pra renderizar PNG no ambiente, entregue o HTML e explique o botão de download.

---

## Atalhos

- `@express` — modo rápido (perguntas mínimas + defaults).
- `@reusar` — pula Fases 1-3 (usuário já tem sistema visual).
- `@tecnico` — explica decisões com mais profundidade (usuário avançado).
- "me mostra" — gera mockup visual da capa com os kits candidatos antes de decidir.

---

## Se algo der errado no build

- Kit desconhecido → confira o nome (um de: editorial, tech, brutalist, serif-classic, clean-sans, warm, playful, corporate).
- Fonte não carrega → o `fontes.css` do kit existe em `assets/kits/{kit}/`? Se não, rode `python assets/gerar_fontes.py {kit}`.
- Texto cortado no slide → encurte o copy ou reduza o número de itens; carrossel é sobre síntese.
- Playwright falha ao instalar → entregue o HTML; o botão de download cobre o caso sem Code Execution.
