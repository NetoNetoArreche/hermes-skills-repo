#!/usr/bin/env python3
"""
gerar_fontes.py — Gera os arquivos fontes.css de cada kit do CARROSSEL PRO,
embutindo as fontes em base64 (woff2) para que o HTML final funcione 100% offline.

Por padrao baixa do Fontsource (registro npm), que costuma estar liberado em
ambientes de execucao. Se voce roda local com acesso ao Google Fonts, pode trocar
a origem facilmente — as familias sao as mesmas.

USO:
    python gerar_fontes.py            # gera todos os kits
    python gerar_fontes.py tech       # gera so um kit
    python gerar_fontes.py --lista    # lista os kits

REQUISITOS: Node/npm disponiveis (usa `npm pack` para baixar os pacotes @fontsource).
"""
import base64, subprocess, sys, tarfile, re
from pathlib import Path

# Curadoria CARROSSEL PRO — 8 kits, cada um com Display / Body / Mono testados juntos.
KITS = {
    "editorial":     [("Anton", [400]), ("Instrument Serif", [(400, "italic")]),
                      ("Inter", [400, 500, 600, 700]), ("JetBrains Mono", [500, 600])],
    "tech":          [("Space Grotesk", [500, 600, 700]),
                      ("Inter", [400, 500, 600, 700]), ("IBM Plex Mono", [400, 500])],
    "brutalist":     [("Archivo", [400, 500, 600, 800, 900]), ("Space Mono", [400, 700])],
    "serif-classic": [("Playfair Display", [400, 700, 900]),
                      ("EB Garamond", [400, 500, 600, 700]), ("Courier Prime", [400, 700])],
    "clean-sans":    [("Manrope", [400, 500, 600, 700, 800]), ("DM Mono", [400, 500])],
    "warm":          [("Fraunces", [400, 600, 700, 900]),
                      ("Karla", [400, 500, 600, 700]), ("DM Mono", [400, 500])],
    "playful":       [("Syne", [500, 600, 700, 800]),
                      ("Manrope", [400, 500, 600, 700]), ("DM Mono", [400, 500])],
    "corporate":     [("Red Hat Display", [400, 500, 600, 700, 900]), ("Red Hat Mono", [400, 500])],
}

OUT_BASE = Path(__file__).parent / "kits"
CACHE = Path("/tmp/cc_fonts_cache"); CACHE.mkdir(exist_ok=True)


def pkg_id(family): return family.lower().replace(" ", "-")


def ensure_pkg(family):
    fid = pkg_id(family)
    tars = list(CACHE.glob(f"fontsource-{fid}-*.tgz"))
    if not tars:
        r = subprocess.run(["npm", "pack", f"@fontsource/{fid}"],
                           cwd=CACHE, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"npm pack falhou para {family}: {r.stderr[-200:]}")
        tars = list(CACHE.glob(f"fontsource-{fid}-*.tgz"))
    with tarfile.open(tars[0]) as t:
        return tars[0], t.getnames(), fid


def weights_disp(members, fid, style):
    pat = re.compile(rf"package/files/{re.escape(fid)}-latin-(\d+)-{style}\.woff2$")
    return sorted({int(m.group(1)) for x in members if (m := pat.search(x))})


def b64_of(tar, fid, w, style):
    with tarfile.open(tar) as t:
        return base64.b64encode(t.extractfile(
            f"package/files/{fid}-latin-{w}-{style}.woff2").read()).decode("ascii")


def face(fam, w, style, b64):
    return (f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{w};"
            f"font-display:swap;src:url(data:font/woff2;base64,{b64}) format('woff2');}}")


def gen(kit_id, fonts):
    parts = []
    for fam, weights in fonts:
        tar, members, fid = ensure_pkg(fam)
        faces = []
        for w in weights:
            weight, style = (w if isinstance(w, tuple) else (w, "normal"))
            avail = weights_disp(members, fid, style)
            if not avail:
                print(f"    ! {fam}: sem peso '{style}'"); continue
            chosen = weight if weight in avail else min(avail, key=lambda a: abs(a - weight))
            faces.append(face(fam, weight, style, b64_of(tar, fid, chosen, style)))
        parts.append(f"/* {fam} */\n" + "\n".join(faces))
        print(f"  ok {fam} ({len(faces)})")
    out = OUT_BASE / kit_id; out.mkdir(parents=True, exist_ok=True)
    (out / "fontes.css").write_text("\n\n".join(parts), encoding="utf-8")
    print(f"=> {kit_id}: {(out/'fontes.css').stat().st_size/1024:.0f} KB\n")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--lista" in sys.argv:
        print("Kits:", ", ".join(KITS)); sys.exit(0)
    for k in (args or KITS):
        print(f"Gerando {k}..."); gen(k, KITS[k])
    print("Pronto.")
