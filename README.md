# meu-emprego: currículo sob medida com 5 agentes de IA

Você manda **o seu currículo em PDF** e **o texto da vaga**. Cinco agentes adaptam o currículo, avaliam como um recrutador, revisam e ainda preparam você para a entrevista.

Funciona com **Claude, ChatGPT, Gemini, Grok, Copilot, DeepSeek** e outros. Sem chave de API: você usa o assistente que já tem.

| # | Agente | O que faz |
|---|---|---|
| 1 | Estrategista de Carreira | Reescreve o resumo e reordena as experiências para a vaga |
| 2 | Gerente de Contratação | Dá nota de 1 a 10, aponta forças, lacunas e palavras-chave |
| 3 | Editor de Currículo | Aplica o feedback sem inventar nada |
| 2 ⇄ 3 | Gerente e Editor | Repetem até a nota 8.5, até 3 revisões, ficando com a melhor versão |
| 4 | Candidato | Relatório com nota final, melhorias e lacunas abertas |
| 5 | Coach de Entrevista | Guia de preparação com 15 perguntas e respostas baseadas no seu currículo |

## Escolha como usar

| Você usa | Caminho | Avaliação independente* |
|---|---|---|
| ChatGPT, Gemini, Grok, Copilot ou DeepSeek no navegador/app | [Opção A: prompt único](#opção-a-qualquer-chat-de-ia) | Não |
| Claude Code | [Opção B: skill](#opção-b-claude-code) | Sim |
| Codex, Gemini CLI, Cursor ou outro agente que lê arquivos | [Opção C: AGENTS.md](#opção-c-codex-gemini-cli-cursor-e-outros) | Depende da ferramenta |

\* Com subagentes, o Gerente é um agente novo que não escreveu o currículo, e a nota fica mais honesta. Sem eles, o mesmo modelo faz todos os papéis em sequência.

### Opção A: qualquer chat de IA

1. Abra [`prompts/00-prompt-unico.md`](prompts/00-prompt-unico.md) e copie o prompt.
2. Numa conversa nova, anexe o seu currículo em PDF, cole o prompt e, no final, a vaga.
3. Pegue o currículo pronto em texto e em JSON. Se o chat executar Python (ex.: ChatGPT), peça o PDF ali mesmo.
4. Se não, gere o PDF no seu computador:
   ```bash
   git clone https://github.com/GuilhermeBorba2/meu-emprego-skill.git
   cd meu-emprego-skill
   pip install reportlab
   python -X utf8 skills/meu-emprego/scripts/render.py caminho/resume.json            # --lang en para inglês
   ```

### Opção B: Claude Code

```bash
git clone https://github.com/GuilhermeBorba2/meu-emprego-skill.git
pip install -r meu-emprego-skill/skills/meu-emprego/scripts/requirements.txt
cp -r meu-emprego-skill/skills/meu-emprego ~/.claude/skills/
```

Depois, em qualquer pasta, abra o Claude Code e diga:

> /meu-emprego — segue meu currículo (caminho/curriculo.pdf) e a vaga: <cole o anúncio>

### Opção C: Codex, Gemini CLI, Cursor e outros

O formato `SKILL.md` segue o padrão aberto de *Agent Skills*. Se a sua ferramenta suporta skills, copie `skills/meu-emprego/` para a pasta de skills dela (veja a documentação da ferramenta).

Se não suporta, clone o repositório e abra o assistente **dentro da pasta**. O [`AGENTS.md`](AGENTS.md) aponta para as instruções, e muitas ferramentas leem esse arquivo sozinhas. Se a sua não ler, diga: *"siga o AGENTS.md"*.

```bash
git clone https://github.com/GuilhermeBorba2/meu-emprego-skill.git
cd meu-emprego-skill
pip install -r skills/meu-emprego/scripts/requirements.txt
```

## O que sai

Nas opções B e C, o resultado fica em `outputs/<voce>/<cargo>_<empresa>/`:

```
json/resume.json             conteúdo do currículo
latex/<nome>_curriculo.tex   versão editável
pdf/<nome>_curriculo.pdf     o currículo final
evaluations/round_N.md       avaliação de cada rodada
coverage_review.md           auditoria de cobertura por posição
rating_report.md             notas, motivo da parada e lacunas abertas
interview_prep.md            preparação para a entrevista
```

Dica: o PDF do seu LinkedIn (Mais ⋯ → Salvar como PDF) junto com o currículo dá mais material para os agentes.

## Regras que nunca mudam

- **Não inventa** empresa, cargo, data, tecnologia nem número. O que a vaga pede e você não tem vira lacuna registrada, não maquiagem.
- Um `profile_truth.md` (criado como rascunho na primeira vez) é a fonte de verdade: corrija-o e liste ali o que nunca pode aparecer.
- **Você revisa e se candidata.** A skill não envia candidaturas.
- `input/`, `data/` e `outputs/` têm dados pessoais e ficam fora do git.

## Feedback

Testou? Abra uma [issue](https://github.com/GuilhermeBorba2/meu-emprego-skill/issues) contando qual IA usou, o que funcionou e o que não funcionou. Sem dados pessoais, por favor.

## Créditos

Baseada no método e no gerador de PDF do [meu-emprego-novo](https://github.com/R238Company/meu-emprego-novo) (Ricardo Martins / R238), por sua vez derivado do trabalho de Rushi Chaudhari. Licença MIT.
