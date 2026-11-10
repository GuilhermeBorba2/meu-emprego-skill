# Instruções para assistentes de IA

Este repositório contém a skill **meu-emprego**: currículo sob medida para uma vaga, feito por 5 agentes (Estrategista, Gerente de Contratação, Editor, Candidato, Coach de Entrevista).

Quando o usuário pedir para adaptar um currículo a uma vaga, preparar entrevista ou "fazer o currículo pra essa vaga", siga **todas** as instruções de [`skills/meu-emprego/SKILL.md`](skills/meu-emprego/SKILL.md). Isso vale para Codex, Gemini CLI, Cursor, Copilot, Claude Code ou qualquer outra ferramenta que leia este arquivo.

Resumo do que nunca muda:
- Peça só o currículo (PDF/DOCX) e a vaga.
- Não invente nada: o que a vaga pede e a pessoa não tem vira lacuna registrada.
- O PDF sai com `python -X utf8 skills/meu-emprego/scripts/render.py outputs/<pessoa>/<slug>`.
- `input/`, `data/` e `outputs/` têm dados pessoais e nunca vão para o git.
- Não se candidate nem preencha formulários pela pessoa.
