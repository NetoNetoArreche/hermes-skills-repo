# 02 — KITS TIPOGRÁFICOS
## 8 sistemas pré-curados, prontos pra usar offline

---

## Por que kits pré-curados

Escolher fonte é o mais difícil pro intermediário — são milhares de famílias e misturar mal arruína o design. Por isso há 8 kits onde Display + Body + Mono já foram testados como conjunto. Não misture fontes entre kits sem motivo forte.

Cada kit tem 3 papéis:
- **Display** — títulos/capa, a fonte "estrela" com personalidade.
- **Body** — corpo de texto, legível.
- **Mono** — kicker, índice, detalhes editoriais e o botão de CTA.

As fontes já estão embutidas em base64 em `assets/kits/{kit_id}/fontes.css`. O motor (`build_carrossel.py`) carrega o kit certo sozinho — você só informa o `kit` no JSON.

---

## Árvore de decisão (por arquétipo)

| Arquétipo | Kit recomendado | Alternativa |
|---|---|---|
| Sábio | `serif-classic` | `editorial` |
| Inocente | `clean-sans` | `warm` |
| Explorador | `brutalist` | `tech` |
| Herói | `brutalist` | `corporate` |
| Fora-da-lei | `brutalist` | `editorial` |
| Mago | `editorial` | `playful` |
| Cara comum | `clean-sans` | `corporate` |
| Amante | `editorial` | `serif-classic` |
| Bobo da corte | `playful` | `clean-sans` |
| Cuidador | `warm` | `clean-sans` |
| Criador | `playful` | `editorial` |
| Governante | `corporate` | `serif-classic` |

Para nicho de **tech / startup / IA / vibe coding**, o default mais seguro é `tech`. Para B2B sério, `corporate`. Para marca pessoal acolhedora, `warm`.

---

## Os 8 kits

### `editorial` — revista/moda, ousado
- Display: Anton (condensada, pesada) · Serif de apoio: Instrument Serif (itálico)
- Body: Inter · Mono: JetBrains Mono
- **Quando:** marca que quer impacto de capa de revista, contraste forte.

### `tech` — startup/SaaS/IA, moderno e limpo
- Display: Space Grotesk · Body: Inter · Mono: IBM Plex Mono
- **Quando:** produto digital, conteúdo técnico, vibe coding. Equilibra moderno + legível.

### `brutalist` — cru, alto impacto
- Display + Body: Archivo (até peso 900) · Mono: Space Mono
- **Quando:** marca que provoca, gancho agressivo, herói/fora-da-lei.

### `serif-classic` — livro de capa dura, autoridade
- Display: Playfair Display · Body: EB Garamond · Mono: Courier Prime
- **Quando:** consultoria, premium, conteúdo de profundidade. Sensação "NY Times".

### `clean-sans` — minimal, amigável
- Display + Body: Manrope · Mono: DM Mono
- **Quando:** marca que quer clareza e simpatia sem firula. Ótimo default neutro.

### `warm` — humana, calorosa (sem clichê)
- Display: Fraunces · Body: Karla · Mono: DM Mono
- **Quando:** coaching, bem-estar, marca pessoal próxima.

### `playful` — criativo, energético
- Display: Syne · Body: Manrope · Mono: DM Mono
- **Quando:** marca jovem, divertida, criativa.

### `corporate` — corporativo, confiança
- Display + Body: Red Hat Display · Mono: Red Hat Mono
- **Quando:** B2B, serviço sério, governante.

---

## Paletas iniciais sugeridas (ajuste à marca)

A paleta vai no JSON em `paleta`. Tokens: `bg` (fundo), `fg` (texto principal), `muted` (texto secundário), `accent` (cor da marca), `surface` (cards/contorno do número fantasma), `cream` (fundo claro de slides "respiro").

| Vibe | bg | fg | muted | accent | surface |
|---|---|---|---|---|---|
| Dark tech | #0A0A0A | #FFFFFF | #8A8A8A | #7C5CFF | #161616 |
| Dark quente | #0E0B08 | #F7F2EA | #9A8E7E | #FF6B35 | #1A1510 |
| Claro minimal | #F7F6F2 | #111111 | #6B6B6B | #2E5BFF | #E7E5DE |
| Premium escuro | #0C0C0E | #F2EBDD | #8E8A82 | #C9A24B | #18181C |

Regras: contraste alto entre `bg` e `fg`; `accent` usado com parcimônia (kicker, régua, número, CTA); slides "respiro" usam `cream` pra dar ritmo no meio do carrossel (`"breather": true`).

---

## Como mostrar opções

Se o usuário pedir pra ver, gere o slide capa com 2 kits candidatos (build com `--no-render` e mostre, ou render rápido). Compare em tabela: kit, vibe, por que encaixa. Deixe ele escolher com critério.
