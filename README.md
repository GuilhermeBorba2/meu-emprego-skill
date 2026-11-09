# meu-emprego — skill para Claude Code

Currículo sob medida para cada vaga, feito pelo próprio Claude com **5 agentes**, sem chave de API.

Você manda **o seu currículo em PDF** e **o texto da vaga**. O Claude faz o resto:

| # | Agente | O que faz |
|---|---|---|
| 1 | Estrategista de Carreira | Reescreve o resumo e reordena as experiências para a vaga |
| 2 | Gerente de Contratação | Dá nota de 1 a 10, aponta forças, lacunas e palavras-chave |
| 3 | Editor de Currículo | Aplica o feedback sem inventar nada |
| 2 ⇄ 3 | Gerente e Editor | Repetem até a nota 8.5, até 3 revisões, ficando com a melhor versão |
| 4 | Candidato | Relatório com nota final, melhorias e lacunas abertas |
| 5 | Coach de Entrevista | Guia de preparação com 15 perguntas e respostas baseadas no seu currículo |

O Gerente é sempre um subagente novo, que não escreveu o currículo, para a avaliação ser independente.

## Instalar

Requisitos: [Claude Code](https://claude.com/claude-code) e Python 3.9+ com `reportlab` (opcional: LaTeX/`pdflatex` para o template completo).

```bash
git clone https://github.com/GuilhermeBorba2/meu-emprego-skill.git
pip install -r meu-emprego-skill/skills/meu-emprego/scripts/requirements.txt
```

Copie a skill para a pasta de skills do Claude Code:

- Para todos os projetos: `~/.claude/skills/meu-emprego/`
- Só para um projeto: `<projeto>/.claude/skills/meu-emprego/`

```bash
cp -r meu-emprego-skill/skills/meu-emprego ~/.claude/skills/
```

## Usar

Numa pasta de trabalho qualquer, abra o Claude Code e diga algo como:

> /meu-emprego — segue meu currículo (caminho/curriculo.pdf) e a vaga: <cole o anúncio>

O Claude pede só o que faltar. O resultado sai em `outputs/<voce>/<cargo>_<empresa>/`:

```
json/resume.json          conteúdo do currículo
latex/<nome>_curriculo.tex   versão editável
pdf/<nome>_curriculo.pdf     o currículo final
evaluations/round_N.md    avaliação de cada rodada
coverage_review.md        auditoria de cobertura por posição
rating_report.md          notas, motivo da parada e lacunas abertas
interview_prep.md         preparação para a entrevista
```

Dica: o PDF do seu LinkedIn (Mais ⋯ → Salvar como PDF) junto com o currículo dá mais material para os agentes.

## Regras que a skill segue

- **Não inventa** empresa, cargo, data, tecnologia nem número. O que a vaga pede e você não tem vira lacuna registrada, não maquiagem.
- Um `profile_truth.md` (criado como rascunho na primeira vez) é a fonte de verdade: corrija-o e liste ali o que nunca pode aparecer.
- **Você revisa e se candidata.** A skill não envia candidaturas.
- `input/`, `data/` e `outputs/` têm dados pessoais e ficam fora do git.

## Créditos

Baseada no método e no gerador de PDF do [meu-emprego-novo](https://github.com/R238Company/meu-emprego-novo) (Ricardo Martins / R238), por sua vez derivado do trabalho de Rushi Chaudhari. Licença MIT.
