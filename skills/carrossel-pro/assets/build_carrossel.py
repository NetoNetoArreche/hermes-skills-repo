#!/usr/bin/env python3
"""
build_carrossel.py — Motor do CARROSSEL PRO.

Recebe um JSON de configuracao (kit + paleta + slides) e gera:
  1) Um HTML standalone (fontes embutidas, funciona offline, com botao de download
     que renderiza os slides em PNG no proprio navegador via html2canvas).
  2) Se o Playwright estiver disponivel: PNGs retina 2x de cada slide + um montage
     2xN para revisao visual rapida.

USO:
    python build_carrossel.py --config slides.json --out ./saida
    python build_carrossel.py --config slides.json --out ./saida --formato 1:1
    python build_carrossel.py --config slides.json --out ./saida --no-render

FORMATO DO JSON (resumo — ver references/05-template-html.md):
{
  "kit": "tech",
  "formato": "4:5",                    # 4:5 (padrao) | 1:1 | 9:16 — tambem via --formato
  "paleta": {"bg":"#0A0A0A","fg":"#FFFFFF","muted":"#8A8A8A","accent":"#7C5CFF",
             "surface":"#141414","cream":"#F2EBDD"},
  "handle": "@seuusuario",
  "logo": "logo.png",                  # opcional — PNG/SVG/JPG/WEBP. Embutido em base64.
  "logo_pos": "capa",                  # "capa" (so na capa) | "todos" (marca em todo slide)
  "logo_altura": 72,
  "logo_inverter_no_claro": false,
  "capa_bg": "fundo_capa.jpg",         # opcional — imagem de fundo da capa (embutida)
  "cta_bg": "fundo_final.jpg",         # opcional — imagem de fundo do slide final
  "bg_overlay": 0.55,                  # escurecimento sobre as fotos (0=claro, 1=preto)
  "slides": [
     {"tipo":"capa","kicker":"GUIA","titulo":"...","sub":"..."},
     {"tipo":"passo","ghost":true,"titulo":"...","corpo":"..."},   # ghost: numero grande de fundo
     {"tipo":"insight","texto":"...","fonte":"..."},
     {"tipo":"lista","titulo":"...","itens":["...","..."]},
     {"tipo":"stat","numero":"3x","rotulo":"...","corpo":"..."},
     {"tipo":"cta","titulo":"...","acao":"...","sub":"...","bg":"foto.jpg"}  # bg por slide
  ]
}

NUMERACAO: o indice do canto (NN/total) e SEMPRE a posicao real do slide.
O numero grande de fundo e decorativo e controlado pela flag `ghost`
(true = numero da posicao; ou uma string para texto livre).
"""
import argparse, base64, html, json, sys
from pathlib import Path

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".svg": "image/svg+xml", ".webp": "image/webp", ".gif": "image/gif"}


def img_data_uri(path, kind="Imagem"):
    """Le um arquivo de imagem e devolve um data: URI base64 (embutido, offline)."""
    p = Path(path)
    if not p.exists():
        sys.exit(f"{kind} nao encontrada: {path}")
    mime = MIME.get(p.suffix.lower())
    if not mime:
        sys.exit(f"Formato nao suportado: {p.suffix}. Use PNG, SVG, JPG, WEBP ou GIF.")
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def logo_data_uri(path):
    return img_data_uri(path, "Logo")


# Formatos do Instagram (largura, altura) em px.
FORMATS = {
    "4:5": (1080, 1350), "retrato": (1080, 1350),
    "1:1": (1080, 1080), "quadrado": (1080, 1080),
    "9:16": (1080, 1920), "stories": (1080, 1920), "reels": (1080, 1920),
}
DEFAULT_FORMAT = "4:5"


def resolve_formato(nome):
    if not nome:
        return FORMATS[DEFAULT_FORMAT]
    key = str(nome).strip().lower()
    if key not in FORMATS:
        sys.exit(f"Formato desconhecido: {nome}. Opcoes: {', '.join(sorted(set(FORMATS)))}")
    return FORMATS[key]


ASSETS = Path(__file__).parent
KITS_DIR = ASSETS / "kits"

# Mapeia cada kit para as familias usadas em --f-display / --f-body / --f-mono
KIT_FAMILIES = {
    "editorial":     ("Anton", "Inter", "JetBrains Mono", "Instrument Serif"),
    "tech":          ("Space Grotesk", "Inter", "IBM Plex Mono", None),
    "brutalist":     ("Archivo", "Archivo", "Space Mono", None),
    "serif-classic": ("Playfair Display", "EB Garamond", "Courier Prime", None),
    "clean-sans":    ("Manrope", "Manrope", "DM Mono", None),
    "warm":          ("Fraunces", "Karla", "DM Mono", None),
    "playful":       ("Syne", "Manrope", "DM Mono", None),
    "corporate":     ("Red Hat Display", "Red Hat Display", "Red Hat Mono", None),
}

DEF_PALETTE = {"bg": "#0A0A0A", "fg": "#FFFFFF", "muted": "#8A8A8A",
               "accent": "#7C5CFF", "surface": "#141414", "cream": "#F2EBDD"}


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def css(kit, pal, serif, w, h):
    disp, body, mono, _ = KIT_FAMILIES[kit]
    serif_fam = serif or body
    return f"""
:root{{
  --bg:{pal['bg']}; --fg:{pal['fg']}; --muted:{pal['muted']};
  --accent:{pal['accent']}; --surface:{pal['surface']}; --cream:{pal['cream']};
  --f-display:'{disp}',system-ui,sans-serif;
  --f-body:'{body}',system-ui,sans-serif;
  --f-mono:'{mono}',ui-monospace,monospace;
  --f-serif:'{serif_fam}',Georgia,serif;
}}
*{{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}}
body{{background:#222;display:flex;flex-direction:column;align-items:center;
  gap:24px;padding:40px;font-family:var(--f-body);}}
.slide{{width:{w}px;height:{h}px;background:var(--bg);color:var(--fg);
  position:relative;overflow:hidden;display:flex;flex-direction:column;
  justify-content:flex-end;padding:96px;text-align:left;}}
.slide *{{text-align:left;}}
.kicker{{font-family:var(--f-mono);font-size:30px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--accent);margin-bottom:28px;}}
.h1{{font-family:var(--f-display);font-size:120px;line-height:.98;
  letter-spacing:-.02em;text-transform:none;}}
.h2{{font-family:var(--f-display);font-size:84px;line-height:1.02;letter-spacing:-.01em;}}
.sub{{font-size:40px;line-height:1.35;color:var(--muted);margin-top:36px;max-width:84%;}}
.body{{font-size:42px;line-height:1.4;color:var(--fg);margin-top:32px;max-width:88%;}}
.ghost{{position:absolute;top:64px;left:96px;font-family:var(--f-display);
  font-size:300px;line-height:1;color:transparent;-webkit-text-stroke:2px var(--surface);
  z-index:0;}}
.idx{{position:absolute;top:96px;right:96px;font-family:var(--f-mono);font-size:30px;
  color:var(--muted);z-index:2;}}
.content{{position:relative;z-index:1;}}
.rule{{width:96px;height:8px;background:var(--accent);margin-bottom:40px;}}
.quote{{font-family:var(--f-serif);font-size:76px;line-height:1.15;font-style:italic;}}
.source{{font-family:var(--f-mono);font-size:30px;color:var(--muted);margin-top:40px;}}
ul.itens{{list-style:none;margin-top:24px;}}
ul.itens li{{font-size:44px;line-height:1.3;padding:28px 0;
  border-bottom:2px solid var(--surface);display:flex;gap:28px;}}
ul.itens li::before{{content:"→";color:var(--accent);font-family:var(--f-mono);}}
.stat{{font-family:var(--f-display);font-size:280px;line-height:.9;color:var(--accent);}}
.rotulo{{font-size:48px;margin-top:8px;}}
.cta{{font-family:var(--f-display);font-size:96px;line-height:1.02;}}
.acao{{display:inline-block;margin-top:48px;background:var(--accent);color:var(--bg);
  font-family:var(--f-mono);font-size:34px;padding:28px 44px;border-radius:14px;
  text-transform:uppercase;letter-spacing:.06em;}}
.handle{{position:absolute;bottom:64px;left:96px;font-family:var(--f-mono);
  font-size:30px;color:var(--muted);}}
.logo{{position:absolute;z-index:3;object-fit:contain;}}
.logo-capa{{top:88px;left:96px;}}
.logo-mark{{bottom:60px;right:96px;opacity:.9;}}
.has-bg .content,.has-bg .ghost{{text-shadow:0 2px 24px rgba(0,0,0,.6);}}
.breather{{background:var(--cream);color:#111;}}
.breather .kicker{{color:var(--accent);}}
.breather .sub,.breather .source,.breather .rotulo{{color:#555;}}
""".strip()


def render_slide(s, total, i, logo=None, bg_uri=None, overlay=0.55, handle=None):
    t = s.get("tipo", "passo")
    has_bg = bool(bg_uri)
    cls = "slide" + (" breather" if s.get("breather") and not has_bg else "") + (" has-bg" if has_bg else "")

    # NUMERAÇÃO: o canto (paginação) é SEMPRE a posição real do slide. Sem contradição.
    idx = f'<div class="idx">{i+1:02d}/{total:02d}</div>'

    # GHOST: número grande de fundo, decorativo. Ligado pela flag `ghost`.
    #   ghost: true  -> mostra o número da posição
    #   ghost: "01"  -> mostra o texto informado
    #   (compat com esquema antigo: se houver `n` e não houver `ghost`, usa `n` como ghost)
    gv = s.get("ghost")
    if gv is None and s.get("n") is not None:
        gv = s.get("n")

    # Logo: sempre na capa; nos demais slides apenas se pos == "todos".
    logo_html = ""
    has_logo_capa = False
    if logo:
        inv = ";filter:invert(1)" if (logo.get("invert") and s.get("breather") and not has_bg) else ""
        if t == "capa":
            logo_html = (f'<img class="logo logo-capa" src="{logo["uri"]}" '
                         f'style="height:{logo["h_capa"]}px{inv}">')
            has_logo_capa = True
        elif logo.get("pos") == "todos":
            logo_html = (f'<img class="logo logo-mark" src="{logo["uri"]}" '
                         f'style="height:{logo["h_mark"]}px{inv}">')

    # ghost só aparece se ligado, sem colidir com logo na capa nem com foto de fundo
    show_ghost = bool(gv) and not has_logo_capa and not has_bg
    ghost_text = gv if isinstance(gv, str) else f"{i+1:02d}"
    ghost = f'<div class="ghost">{esc(ghost_text)}</div>' if show_ghost else ""

    if t == "capa":
        kick = f'<div class="kicker">{esc(s["kicker"])}</div>' if s.get("kicker") else ""
        sub = f'<div class="sub">{esc(s["sub"])}</div>' if s.get("sub") else ""
        hand = f'<div class="handle">{esc(handle)}</div>' if handle else ""
        inner = f'{logo_html}{ghost}{hand}<div class="content">{kick}<div class="h1">{esc(s["titulo"])}</div>{sub}</div>'
    elif t == "insight":
        src = f'<div class="source">{esc(s["fonte"])}</div>' if s.get("fonte") else ""
        inner = f'{idx}<div class="content"><div class="rule"></div><div class="quote">{esc(s["texto"])}</div>{src}</div>'
    elif t == "lista":
        li = "".join(f"<li>{esc(x)}</li>" for x in s.get("itens", []))
        inner = f'{idx}<div class="content"><div class="h2">{esc(s["titulo"])}</div><ul class="itens">{li}</ul></div>'
    elif t == "stat":
        body = f'<div class="body">{esc(s["corpo"])}</div>' if s.get("corpo") else ""
        inner = f'{idx}<div class="content"><div class="stat">{esc(s["numero"])}</div><div class="rotulo">{esc(s.get("rotulo",""))}</div>{body}</div>'
    elif t == "cta":
        acao = f'<div class="acao">{esc(s["acao"])}</div>' if s.get("acao") else ""
        sub = f'<div class="sub">{esc(s["sub"])}</div>' if s.get("sub") else ""
        inner = f'<div class="content"><div class="cta">{esc(s["titulo"])}</div>{sub}{acao}</div>'
    else:  # passo
        body = f'<div class="body">{esc(s["corpo"])}</div>' if s.get("corpo") else ""
        inner = f'{idx}{ghost}<div class="content"><div class="rule"></div><div class="h2">{esc(s["titulo"])}</div>{body}</div>'

    bg_style = ""
    if has_bg:
        o = float(overlay)
        bg_style = (f' style="background:linear-gradient(to top,'
                    f'rgba(0,0,0,{o}),rgba(0,0,0,{o*0.5:.3f}) 55%,'
                    f'rgba(0,0,0,{o*0.15:.3f}) 100%),url({bg_uri}) center/cover;"')

    extra = logo_html if t != "capa" else ""
    return f'<div class="{cls}" id="slide-{i}"{bg_style}>{inner}{extra}</div>'


def build_editor(cfg, w, h):
    """Gera o HTML do EDITOR VISUAL (arrastar texto, trocar fundo, overlay, exportar)."""
    kit = cfg.get("kit", "tech")
    if kit not in KIT_FAMILIES:
        sys.exit(f"Kit desconhecido: {kit}")
    pal = {**DEF_PALETTE, **cfg.get("paleta", {})}
    fontes = (KITS_DIR / kit / "fontes.css").read_text(encoding="utf-8")
    disp, body, mono, serif = KIT_FAMILIES[kit]
    logo = None
    if cfg.get("logo"):
        hh = cfg.get("logo_altura", 72)
        logo = {"uri": logo_data_uri(cfg["logo"]), "pos": cfg.get("logo_pos", "capa"),
                "h_capa": hh, "h_mark": min(hh, 44),
                "invert": cfg.get("logo_inverter_no_claro", False)}
    capa_bg = img_data_uri(cfg["capa_bg"], "Imagem de capa") if cfg.get("capa_bg") else None
    cta_bg = img_data_uri(cfg["cta_bg"], "Imagem do final") if cfg.get("cta_bg") else None
    slides_out = []
    for s in cfg.get("slides", []):
        s2 = dict(s)
        if s.get("bg"):
            s2["bg_uri"] = img_data_uri(s["bg"], "Imagem de fundo")
        elif s.get("tipo") == "capa" and capa_bg:
            s2["bg_uri"] = capa_bg
        elif s.get("tipo") == "cta" and cta_bg:
            s2["bg_uri"] = cta_bg
        else:
            s2["bg_uri"] = None
        slides_out.append(s2)
    config = {
        "w": w, "h": h, "palette": pal,
        "fonts": {"display": disp, "body": body, "mono": mono, "serif": serif or body},
        "handle": cfg.get("handle", ""), "logo": logo,
        "bg_overlay": cfg.get("bg_overlay", 0.55), "slides": slides_out,
    }
    tpl = (ASSETS / "editor_template.html").read_text(encoding="utf-8")
    tpl = tpl.replace("/*__FONTS__*/", fontes)
    tpl = tpl.replace("/*__CONFIG__*/{}", json.dumps(config, ensure_ascii=False))
    return tpl


def build_html(cfg, w, h):
    kit = cfg.get("kit", "tech")
    if kit not in KIT_FAMILIES:
        sys.exit(f"Kit desconhecido: {kit}. Opcoes: {', '.join(KIT_FAMILIES)}")
    pal = {**DEF_PALETTE, **cfg.get("paleta", {})}
    fontes = (KITS_DIR / kit / "fontes.css").read_text(encoding="utf-8")
    serif = KIT_FAMILIES[kit][3]
    slides = cfg.get("slides", [])
    total = len(slides)
    handle = cfg.get("handle", "")
    overlay = cfg.get("bg_overlay", 0.55)

    logo = None
    if cfg.get("logo"):
        hh = cfg.get("logo_altura", 72)
        logo = {
            "uri": logo_data_uri(cfg["logo"]),
            "pos": cfg.get("logo_pos", "capa"),
            "h_capa": hh,
            "h_mark": min(hh, 44),
            "invert": cfg.get("logo_inverter_no_claro", False),
        }

    # Imagens de fundo: capa, final (cta) e/ou por slide (campo "bg").
    capa_bg = img_data_uri(cfg["capa_bg"], "Imagem de capa") if cfg.get("capa_bg") else None
    cta_bg = img_data_uri(cfg["cta_bg"], "Imagem do final") if cfg.get("cta_bg") else None

    parts = []
    for i, s in enumerate(slides):
        bg = None
        if s.get("bg"):
            bg = img_data_uri(s["bg"], "Imagem de fundo")
        elif s.get("tipo") == "capa" and capa_bg:
            bg = capa_bg
        elif s.get("tipo") == "cta" and cta_bg:
            bg = cta_bg
        parts.append(render_slide(s, total, i, logo, bg, overlay, handle))
    body = "\n".join(parts)

    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Carrossel</title><style>{fontes}</style><style>{css(kit, pal, serif, w, h)}
.bar{{position:fixed;top:0;left:0;right:0;background:#7C5CFF;color:#fff;
  font-family:system-ui;padding:14px;text-align:center;z-index:99;cursor:pointer;}}
@media print{{.bar{{display:none}}}}</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
</head><body>
<div class="bar" onclick="baixar()">⬇ BAIXAR OS {total} SLIDES (PNG)</div>
<div style="height:20px"></div>
{body}
<script>
async function baixar(){{
  const slides=document.querySelectorAll('.slide');
  for(let i=0;i<slides.length;i++){{
    const c=await html2canvas(slides[i],{{scale:2,useCORS:true,backgroundColor:null}});
    const a=document.createElement('a');
    a.download='slide-'+String(i+1).padStart(2,'0')+'.png';
    a.href=c.toDataURL('image/png');a.click();
    await new Promise(r=>setTimeout(r,300));
  }}
}}
</script></body></html>"""


def render_pngs(html_path, out_dir, total, w, h):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright nao instalado — pulei o render. Use o botao do HTML no navegador,"
              " ou: pip install playwright && playwright install chromium")
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        pg.goto(f"file://{html_path.resolve()}")
        pg.add_style_tag(content=".bar{display:none!important}")
        pg.wait_for_timeout(800)
        for i in range(total):
            el = pg.query_selector(f"#slide-{i}")
            el.screenshot(path=str(out_dir / f"slide-{i+1:02d}.png"))
        b.close()
    print(f"Renderizados {total} PNGs em {out_dir} ({w}x{h})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", default="./saida")
    ap.add_argument("--formato", help="4:5 (padrao) | 1:1 | 9:16. Sobrepoe o 'formato' do JSON.")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--no-editor", action="store_true", help="nao gera o editor visual")
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    w, h = resolve_formato(a.formato or cfg.get("formato"))
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    html_path = out / "carrossel.html"
    html_path.write_text(build_html(cfg, w, h), encoding="utf-8")
    print(f"HTML: {html_path}  | formato {w}x{h}")
    if not a.no_editor:
        ed_path = out / "carrossel-editor.html"
        ed_path.write_text(build_editor(cfg, w, h), encoding="utf-8")
        print(f"EDITOR: {ed_path}  (abra no navegador pra ajustar fundo/textos/overlay)")
    if not a.no_render:
        render_pngs(html_path, out / "png", len(cfg.get("slides", [])), w, h)


if __name__ == "__main__":
    main()
