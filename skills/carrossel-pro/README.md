# CARROSSEL PRO

Diretor de arte + redator que produz carrosséis de Instagram prontos pra publicar, construindo do zero o sistema visual da sua marca. Em português do Brasil, **100% autônomo** — sem depender de nenhum conector externo.

## O que entrega
- Sistema visual da sua marca (tipografia, paleta, voz) do zero
- **Seu logo embutido** nos slides (só na capa ou como marca d'água em todos)
- Copy slide a slide, com gancho que para o scroll
- HTML standalone que funciona offline (fontes embutidas)
- PNGs retina 2x (1080×1350) prontos pra subir
- **Editor visual** (HTML offline) pra ajustar fundo, posição dos textos, overlay e exportar
- Legenda + hashtags na voz da sua marca
- Um sistema visual salvo pra reutilizar nos próximos carrosséis

## Como ativar
Diga algo como:
- "Quero fazer um carrossel de Instagram pra minha marca"
- "Me ajuda com slides pra IG sobre [tema]"
- "Usa a skill carrossel-pro pra criar um carrossel sobre [tema]"

## Estrutura
```
carrossel-pro/
├── SKILL.md
├── references/        # base de conhecimento (marca, kits, voz, frameworks, técnico, workflow)
└── assets/
    ├── build_carrossel.py   # motor: JSON -> HTML + PNGs
    ├── gerar_fontes.py      # (re)gera as fontes embutidas dos kits
    ├── exemplo_slides.json  # config de exemplo
    └── kits/                # 8 kits tipográficos, fontes embutidas em base64
```

## Requisitos
- **Artifacts / arquivos:** pra receber o HTML e os PNGs.
- **Code Execution:** pra renderizar os PNGs automaticamente (via Playwright).
- **Sem Code Execution:** ainda funciona — abra o HTML no navegador e use o botão "⬇ Baixar os slides".

## Fontes
Todas open-source (Google Fonts via Fontsource — licenças OFL/Apache), embutidas em base64 pra o HTML funcionar sem internet.

## Os 8 kits
editorial · tech · brutalist · serif-classic · clean-sans · warm · playful · corporate
