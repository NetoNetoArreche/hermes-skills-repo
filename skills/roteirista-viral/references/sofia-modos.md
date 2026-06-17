# Modos de Operação (estilo SOFIA)

O curso ensina a usar a IA de roteiros (SOFIA) de duas formas. Esta skill reproduz as duas — já adaptadas ao nicho do Helio — e é assim que ela deve operar quando ele pede algo.

---

## MODO 1 — Criar (Copiar & Colar / gerar a partir do formato)

Equivale ao fluxo "Copiar & Colar" da SOFIA: escolher um formato, pegar o roteiro-modelo + prompt, colocar o nicho e gerar.

Fluxo da skill:
1. Identifica (ou recomenda) o **formato visual** e a **estrutura de roteiro** — ver `formatos-visuais.md` e `estruturas-roteiro.md`.
2. Aplica o **tema** no nicho do Helio — ver `nicho-vibecoding.md`.
3. Escreve o roteiro, **lapida com gatilhos** (ver `gatilhos-e-lapidacao.md`) e entrega no template de saída do SKILL.md.
4. Se for anúncio, aplica `meta-ads.md`.

Gatilhos de ativação (frases típicas do Helio):
- "cria um post no formato Tela Dividida sobre [tema]"
- "me dá um roteiro Cine com tema universal"
- "faz um anúncio AIDA pro Criando Startup"
- "quero uma leva de 3 no formato Narrado"
- "modela esse viral pro meu nicho: [cola roteiro ou link]" → ver `modelos-copia-cola.md`

**Modelar a partir de referência:** quando o Helio trouxer um roteiro/reel que viralizou, NÃO crie do zero — use o motor em `references/modelos-copia-cola.md`: mantenha o esqueleto (estrutura + gatilhos) e troque o tema pro nicho, seguindo as regras anti-ficção (só pessoas/casos reais e verificáveis, com fonte pesquisada e citada).

**Comportamento padrão:** entrega o roteiro direto, assumindo um formato/estrutura bons quando ele não especifica, e deixando claro o que assumiu. Só mostra o menu de seleção (abaixo) se ele pedir ou disser que está em dúvida.

Menu de seleção (quando ele quiser escolher):
- **Formato visual (16):** Tela Dividida · Tela Verde · Narrado · Palestrinha · Cine · Storytelling Visual · Conflito Situacional · Experimento Social · Caixinha de Perguntas · Dinamismo · Comparação · Diálogo · Trivial · The Office · Lo-Fi · Bastidores
- **Estrutura:** AIDA · Jeito Errado/Jeito Certo · IHC · Ele, Eu, Você e o Futuro · Análise · Tríade · Começo-Meio-Fim
- **Tipo de tema:** Universal · Cultura Pop · Tema do Momento (pode combinar 2-3)
- **Saída:** 1 roteiro afiado · leva de 3 (pra lapidar)

---

## MODO 2 — Revisar (análise frase a frase)

Equivale ao fluxo "Revisar seus roteiros" da SOFIA: o Helio escreve o roteiro, manda, e recebe feedback prático frase a frase.

Quando ele colar um roteiro e pedir análise/revisão/feedback, a skill deve:

1. **Quebrar o roteiro em frases/blocos** e comentar cada um, na ordem.
2. Para cada frase, avaliar contra os mecanismos do curso:
   - **Gancho:** tem promessa (curiosidade + conflito + relevância emocional)? Prende em 3s?
   - **Tom:** é de conexão (aprendiz/percepção) ou está apontando o dedo (imperativo)? — apontar o dedo é erro.
   - **Gatilhos:** tem contraste (uso de "mas"), conflito, familiaridade, curiosidade?
   - **Clareza:** a imagem/visual reforça o que a fala diz? Reduz o esforço de entender?
   - **Ritmo:** a frase pode ser cortada/encurtada? Tem respiro sobrando?
   - **Efeito Aha:** o fim entrega uma descoberta?
   - **Para anúncio (se for):** respeita a regra de abrir longe do produto? CTA único? Política ok?
3. **Apontar os 3 erros mortais** se aparecerem: sem promessa, tom imperativo, sem efeito Aha.
4. Entregar a **versão lapidada** do roteiro ao final, já com as melhorias aplicadas.
5. Sugerir **qual 1 mecanismo** focar na próxima leva (princípio: melhora um por vez).

Formato da revisão:
```
ANÁLISE FRASE A FRASE

[frase 1 do usuário]
→ o que funciona / o que ajustar (mecanismo)

[frase 2 do usuário]
→ ...

DIAGNÓSTICO RÁPIDO
- Promessa: ok / fraca
- Tom: conexão / imperativo
- Efeito Aha: tem / falta
- Gatilho mais ausente: [...]

VERSÃO LAPIDADA
[roteiro reescrito, pronto pra gravar]

PRÓXIMO PASSO
Melhore só isto na próxima: [1 mecanismo]
```

Regra de ouro da revisão: ser específico e prático, nunca genérico. Cada comentário deve apontar o mecanismo do curso e como corrigir — não "ficou bom", mas "aqui falta contraste, troca por 'X mas Y'".
