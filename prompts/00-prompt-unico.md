# Prompt único: ChatGPT, Gemini, Grok, Copilot, DeepSeek...

Use este prompt em qualquer chat de IA, inclusive na versão grátis. Ele faz os 5 agentes em sequência, na mesma conversa.

**Como usar:**
1. Abra uma conversa nova.
2. Anexe o seu currículo em PDF (e, se quiser, o PDF do LinkedIn: Mais ⋯ → Salvar como PDF).
3. Copie tudo o que está entre as linhas `---` abaixo, cole no chat e, no final, cole o texto da vaga.
4. Quando ele terminar, peça o PDF (se o chat executar código) ou gere localmente com o `render.py` (veja o README).

> Se o chat não lê PDF, copie o texto do currículo e cole no lugar do anexo.

---

Você vai trabalhar como uma equipe de 5 agentes para adaptar o meu currículo (anexado) a uma vaga (no fim desta mensagem). Faça as etapas na ordem e mostre o resultado de cada uma com um título.

## REGRA DE OURO (vale para todos os agentes)
- Use só o que está no meu currículo/anexos. Nunca invente empresa, cargo, data, tecnologia, certificação ou número. Métrica só se o número exato estiver no meu material.
- O que a vaga pede e eu não tenho é LACUNA: liste, não coloque no currículo.
- Mantenha todas as minhas experiências, da mais recente para a mais antiga. Dentro de cada uma, o mais relevante para a vaga primeiro.
- Escreva em português do Brasil, primeira pessoa no passado ("Desenvolvi", "Liderei"), nunca terceira pessoa ("Desenvolveu"). Só nomes de tecnologia em inglês. (Se a vaga for em inglês e eu pedir, escreva em inglês: "Developed", "Led".)
- Nada de documentos, endereço completo ou dados pessoais além de nome, e-mail, telefone, cidade e links profissionais.

## AGENTE 1: Estrategista de Carreira
Reescreva meu currículo para a vaga:
- Resumo de 3 a 4 frases falando com as prioridades da vaga.
- Título profissional alinhado ao cargo, sem prometer o que não tenho.
- Bullets com verbo de ação (método STAR quando der), usando os termos da vaga só onde for verdade.
- Competências reordenadas: as que a vaga pede primeiro. Não adicione nenhuma que eu não tenha. Nomes de categoria curtos (até ~15 caracteres).
- Liste antes os termos importantes da vaga e marque quais eu tenho (✅) e quais são lacuna (❌).

## AGENTE 2: Gerente de Contratação (avaliação 1)
Agora finja que você NÃO escreveu o currículo acima. Avalie como um recrutador técnico exigente:
- Nota de 1 a 10 com justificativa.
- 3 a 5 pontos fortes.
- 3 a 5 lacunas: por que importam e como tratar DE FORMA VERDADEIRA, ou "lacuna real".
- Palavras-chave da vaga que faltam.
- Procure primeiro qualquer frase sem base no meu material e aponte como erro grave.
- Termine com a linha: NOTA: X.X

## AGENTE 3: Editor de Currículo
Se a nota for menor que 8.5, aplique as sugestões verdadeiras e corrija o que o Gerente apontou. Lacuna real continua lacuna. Depois, repita o AGENTE 2 (nova avaliação, sem olhar a anterior) e o AGENTE 3, até:
- a nota chegar a 8.5; ou
- uma revisão não subir a nota; ou
- 3 revisões.
Fique com a versão de MAIOR nota. Mostre uma tabela: rodada → nota.
Ficar abaixo de 8.5 é um resultado válido quando a lacuna é real: não force.

## AGENTE 4: Candidato (relatório)
Relatório curto: nota final e se bateu 8.5 (igual à tabela), principais melhorias, lacunas que continuam abertas, e o que eu devo conferir antes de enviar.

## AGENTE 5: Coach de Entrevista
Guia de preparação:
- Os 3 requisitos que mais pesam na vaga.
- 15 perguntas prováveis (5 técnicas, 5 comportamentais, 3 situacionais, 2 de motivação), cada uma com: por que perguntam, resposta sugerida baseada SÓ na minha experiência real (use "[substitua por um exemplo real seu]" quando faltar história) e 2–3 pontos-chave. Para lacunas, resposta honesta e como eu aprenderia.
- 2 a 3 pontos fracos que o entrevistador pode notar e como tratar.
- 8 perguntas para eu fazer ao entrevistador.
- O que estudar antes da entrevista.

## ENTREGA FINAL
1. O currículo final em JSON válido, neste formato (sem comentários):
```json
{"basics":{"name":"","label":"","email":"","phone":"","url":"","summary":"","location":{"city":"","region":"","countryCode":""},"profiles":[{"network":"","username":"","url":""}]},
 "work":[{"name":"","position":"","location":"","startDate":"AAAA-MM","endDate":"AAAA-MM ou Present","highlights":[""]}],
 "education":[{"institution":"","area":"","studyType":"","startDate":"","endDate":""}],
 "skills":[{"name":"","keywords":[""]}],
 "certificates":[{"name":"","issuer":"","date":""}],
 "projects":[{"name":"","description":"","highlights":[""],"keywords":[""]}],
 "languages":[{"language":"","fluency":""}]}
```
2. O mesmo currículo em texto formatado, pronto para colar num editor.
3. Se você consegue executar Python: gere um PDF limpo de 1 a 2 páginas (A4, bullets com recuo, títulos de seção em destaque) a partir do JSON, com o nome `<primeiro_nome>_curriculo.pdf`, e me dê o link para baixar.

VAGA:
[cole aqui o texto da vaga]

---

## Gerar o PDF no seu computador

Se o chat não gerou o PDF, salve o JSON como `resume.json` e rode:

```bash
pip install reportlab
python -X utf8 skills/meu-emprego/scripts/render.py resume.json
```

O PDF sai em `pdf/<seu_nome>_curriculo.pdf`, na mesma pasta do JSON.
