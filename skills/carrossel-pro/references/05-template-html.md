# 05 — slides.json e entrega no Carousel Studio

A entrega é o editor **Carousel Studio** (`assets/carousel-studio.html`) já populado.
Você monta um `slides.json` e **injeta** no editor (não há motor de build).

## Formato do slides.json
```json
{
  "kit": "editorial",
  "formato": "4:5",
  "paleta": { "bg":"#E9E1D2","fg":"#1B1714","muted":"#6E6357","accent":"#BE4D2E","surface":"#1B1714","cream":"#F7F2E8" },
  "handle": "@usuario",
  "slides": [ ... ]
}
```
- `kit`: editorial | tech | brutalist | serif-classic | clean-sans | warm | playful | corporate
- `formato`: "4:5" (retrato) | "1:1" (quadrado) | "9:16" (stories)

## Tipos de slide
- `capa`: { "tipo":"capa", "kicker":"GUIA", "titulo":"...", "sub":"...", "ghost":"01" }
- `passo`: { "tipo":"passo", "titulo":"...", "corpo":"...", "ghost":"01", "breather": true }
- `insight`: { "tipo":"insight", "texto":"frase forte", "fonte":"atribuição" }
- `lista`: { "tipo":"lista", "titulo":"...", "itens":["a","b","c"] }
- `stat`: { "tipo":"stat", "numero":"90min", "rotulo":"...", "corpo":"..." }
- `cta`: { "tipo":"cta", "titulo":"...", "acao":"botão", "sub":"..." }

(`ghost` e `breather` são opcionais. `ghost` liga o número gigante de fundo.)

## Injeção (a entrega)
```python
import json
tpl = open(SKILL_DIR + "/assets/carousel-studio.html", encoding="utf-8").read()
dados = json.dumps(MEU_DICT, ensure_ascii=False)
tpl = tpl.replace('<script id="deck-data" type="application/json"></script>',
                  '<script id="deck-data" type="application/json">' + dados + '</script>')
open(PASTA_SAIDA + "/carrossel-editor.html", "w", encoding="utf-8").write(tpl)
```
Apresente o `carrossel-editor.html`. Tudo (edição, fontes, cores, posicionamento, imagem de fundo, cantos, logo e **Exportar ZIP**) acontece dentro dele. NÃO use `build_carrossel.py` nem `editor_template.html` — foram removidos.

## Tipos de card (estilo notícia/anúncio)
- `tweet`: card de post/rede social.
  ```json
  { "tipo":"tweet", "titulo":"Headline opcional", "sub":"linha opcional",
    "autor":"Claude", "handle":"@claudeai", "verificado":true,
    "texto":"Texto do post. Use **palavra** pra realçar.",
    "img":"(opcional)", "likes":"1,8k", "rts":"205", "replies":"96", "views":"1,7M" }
  ```
- `nota`: card de aviso/nota.
  ```json
  { "tipo":"nota", "titulo":"Headline opcional",
    "icone":"lock|shield|info|alert|star|check|sparkles",
    "cardTitulo":"Título do card", "cardTexto":"Texto do card." }
  ```
