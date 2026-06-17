# 05 — TEMPLATE HTML, JSON E MOTOR
## Como o carrossel é construído tecnicamente

---

## Visão geral

O motor é `assets/build_carrossel.py`. Você não escreve HTML na mão — você monta um **JSON de configuração** e roda o script. Ele:
1. Carrega as fontes embutidas do kit escolhido (`assets/kits/{kit}/fontes.css`).
2. Aplica a paleta via CSS variables.
3. Gera `carrossel.html` standalone (offline, com botão de download via html2canvas).
4. Se o Playwright existir, renderiza os PNGs retina 2x (`png/slide-01.png`...).

Formatos suportados: **4:5** (1080×1350, retrato — padrão), **1:1** (1080×1080, quadrado) e **9:16** (1080×1920, stories/reels).

---

## Formato do JSON

```json
{
  "kit": "tech",
  "formato": "4:5",
  "paleta": {
    "bg": "#0A0A0A", "fg": "#FFFFFF", "muted": "#8A8A8A",
    "accent": "#7C5CFF", "surface": "#161616", "cream": "#F2EBDD"
  },
  "handle": "@seuusuario",
  "logo": "logo.png",
  "logo_pos": "capa",
  "logo_altura": 72,
  "logo_inverter_no_claro": false,
  "capa_bg": "fundo_capa.jpg",
  "cta_bg": "fundo_final.jpg",
  "bg_overlay": 0.55,
  "slides": [ ... ]
}
```

- `kit`: um de `editorial, tech, brutalist, serif-classic, clean-sans, warm, playful, corporate`.
- `formato`: `"4:5"` (padrão), `"1:1"` ou `"9:16"`. Também pode vir pela flag `--formato`.
- `paleta`: qualquer token omitido usa o default. Veja paletas em `02-kits-tipograficos.md`.
- `handle`: carimbado discretamente na capa.

---

## Imagem de fundo (opcional)

Dá pra colocar foto/arte de fundo na capa, no slide final e/ou em qualquer slide. A imagem é embutida em base64 (offline) e recebe um gradiente escuro por cima pra o texto continuar legível.

- `capa_bg`: imagem de fundo da capa.
- `cta_bg`: imagem de fundo do slide final (cta).
- `bg` (por slide): `{"tipo":"passo","bg":"foto.jpg", ...}` — fundo só naquele slide.
- `bg_overlay`: 0 a 1, quanto escurecer a foto (default 0.55; suba pra 0.7 se o texto estiver difícil de ler).

Quando um slide tem foto de fundo, o número fantasma é suprimido (pra não competir com a imagem).

---

## Logo / identidade visual (opcional)

Se o usuário tem logo, embuta nos slides. O arquivo é lido e convertido em base64 (fica embutido, funciona offline). Formatos: PNG (ideal com fundo transparente), SVG, JPG, WEBP, GIF.

Campos no JSON:
- `logo`: caminho do arquivo do logo. Salve o upload do usuário num caminho e aponte aqui.
- `logo_pos`: `"capa"` (só no primeiro slide, grande, canto superior esquerdo — e o número fantasma da capa é suprimido pra não colidir) ou `"todos"` (marca pequena no canto inferior direito de TODOS os slides). Default: `"capa"`.
- `logo_altura`: altura em px do logo na capa (default 72). A marca dos demais slides usa `min(altura, 44)`.
- `logo_inverter_no_claro`: `true` se o logo é claro/branco — assim ele é invertido (vira escuro) automaticamente nos slides de fundo claro (`breather`), pra não sumir. Default `false`.

Dica: peça um logo horizontal ou um símbolo compacto. Logos muito detalhados ficam ilegíveis em tamanho pequeno na marca d'água.

---

## Tipos de slide

Cada item de `slides` tem um `tipo`. Campos por tipo:

**`capa`** — o primeiro slide.
```json
{"tipo":"capa","kicker":"GUIA","titulo":"Título grande","sub":"Subtítulo opcional"}
```
`kicker` é o rótulo mono em cima. (A capa não usa número.)

**`passo`** — slide de conteúdo padrão (régua de acento + título + corpo).
```json
{"tipo":"passo","ghost":true,"titulo":"Título do passo","corpo":"1-3 linhas."}
```
`ghost` (opcional) liga o número grande de fundo — veja "Numeração" abaixo.

**`insight`** — frase de destaque (itálico serifado/grande).
```json
{"tipo":"insight","texto":"Uma frase forte que sintetiza a ideia.","fonte":"opcional"}
```

**`lista`** — título + itens com seta.
```json
{"tipo":"lista","titulo":"O que checar","itens":["Item um","Item dois","Item três"]}
```

**`stat`** — número grande + rótulo + corpo.
```json
{"tipo":"stat","numero":"3x","rotulo":"mais rápido","corpo":"explicação curta"}
```

**`cta`** — fechamento com botão.
```json
{"tipo":"cta","titulo":"Salva esse post","acao":"Me segue pra mais","sub":"linha de apoio"}
```

Qualquer slide aceita `"breather": true` → fundo claro (`cream`), pra dar respiro/ritmo no meio do carrossel. E `"bg": "foto.jpg"` → foto de fundo só naquele slide.

---

## Numeração (importante)

São duas coisas independentes:

- **Índice do canto** (`NN/total`, topo direito): é a **paginação** e vem SEMPRE da posição real do slide. Não dá pra forçar — assim nunca há contradição (o slide 3 mostra `03`, ponto).
- **Número fantasma** (número grande translúcido no fundo): é **decorativo** e ligado pela flag `ghost`:
  - `"ghost": true` → mostra o número da posição do slide.
  - `"ghost": "01"` → mostra o texto que você quiser (ex.: numerar passos à parte da capa).
  - sem `ghost` → não aparece número de fundo.

O número fantasma é suprimido automaticamente quando o slide tem foto de fundo ou logo grande na capa.

---

## Rodando o motor

```bash
# gera HTML + PNGs (se Playwright instalado)
python assets/build_carrossel.py --config slides.json --out ./saida

# escolher formato (sobrepõe o "formato" do JSON)
python assets/build_carrossel.py --config slides.json --out ./saida --formato 1:1

# só o HTML (sem render — mais rápido, pra preview rápido)
python assets/build_carrossel.py --config slides.json --out ./saida --no-render
```

Saídas:
- `saida/carrossel.html` — abre em qualquer navegador; botão "⬇ Baixar os slides" gera os PNGs no próprio navegador (caminho sem Code Execution).
- `saida/carrossel-editor.html` — **editor visual** (veja abaixo).
- `saida/png/slide-01.png ...` — PNGs 2x retina, prontos pra subir no Instagram (só quando Playwright está disponível).

---

## Editor visual (carrossel-editor.html)

Toda geração também produz um **editor** que o usuário abre no navegador (offline, sem instalar nada) pra dar os ajustes finos sem mexer em código:

- **Imagem de fundo por slide:** clica no slide, "Escolher" → seleciona a foto do computador (vira fundo com overlay).
- **Overlay:** controle deslizante pra escurecer/clarear a foto (legibilidade do texto).
- **Mover textos:** clica num texto e arrasta pra reposicionar. Dois cliques pra editar o conteúdo.
- **Cor de acento:** seletor de cor no topo, muda em todos os slides.
- **Fundo claro (respiro):** caixinha pra alternar o slide pra fundo creme.
- **+ Texto:** adiciona um bloco de texto novo no slide ativo.
- **Exportar PNGs:** renderiza todos os slides em PNG 2x ali no navegador.

Pra desligar a geração do editor: `--no-editor`. O editor é montado a partir do `assets/editor_template.html` (as fontes e o conteúdo são injetados na hora).

Se o Playwright não estiver no ambiente:
```bash
pip install playwright && playwright install chromium
```
Se nem isso for possível, entregue o HTML e oriente o usuário a usar o botão de download no navegador dele.

---

## Regenerar as fontes (raro)

Os kits já vêm prontos em `assets/kits/`. Só precisa rodar se quiser recriar ou adicionar pesos:
```bash
python assets/gerar_fontes.py            # todos
python assets/gerar_fontes.py tech       # um kit
```
Baixa do Fontsource (npm). As fontes são open-source (OFL/Apache).

---

## Boas práticas de layout

- Capa: pouco texto, muito respiro. O título é a estrela.
- 1 ideia por slide. Corpo curto.
- Use `breather` 1x no meio de carrosséis longos (8+).
- `accent` com parcimônia — ele perde força se estiver em tudo.
- Não sobrescreva `text-align`. Tudo é alinhado à esquerda por decisão de design (leitura mais fácil em carrossel).
