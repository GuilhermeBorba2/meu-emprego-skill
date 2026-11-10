---
name: meu-emprego
description: Gera currículo sob medida para uma vaga (JSON → LaTeX → PDF), com avaliação de aderência, revisão de cobertura e preparação de entrevista, com 5 agentes (Estrategista, Gerente, Editor, Candidato, Coach) que funcionam em qualquer assistente de IA com acesso a arquivos (Claude Code, Codex, Gemini CLI, Cursor e similares), sem chave de API extra. Use quando o usuário colar uma vaga e pedir currículo, adaptar currículo, "faz pra essa vaga", preparar entrevista, ou extrair currículo de PDFs para data/<pessoa>/resume.json.
---

# meu-emprego: currículo sob medida com 5 agentes de IA

Você orquestra 5 agentes que fazem todo o trabalho de texto. Funciona com qualquer modelo (Claude, GPT, Gemini, Grok...). O único código executado é o renderizador de PDF em `scripts/render.py` desta skill (Python + `reportlab`).

Área de trabalho = diretório atual da sessão. Use as pastas `input/<p>/` (arquivos do usuário), `data/<p>/` (base) e `outputs/<p>/` (resultados); crie se não existirem. Esses dados são pessoais: se o diretório for um repositório git, garanta que `input/`, `data/` e `outputs/` estejam no `.gitignore`.

`<dir-da-skill>` = a pasta onde está este SKILL.md (no repositório clonado: `skills/meu-emprego`).

Python: use `python` (ou `py -3` no Windows). Se `import reportlab` falhar, rode `python -m pip install -r <dir-da-skill>/scripts/requirements.txt`.

Arquivos temporários (ex.: imagens da checagem visual): use a pasta temporária da sua ferramenta ou `outputs/<p>/<slug>/_tmp/` e apague no fim. Nunca grave nada fora de `input/`, `data/` e `outputs/`.

## Regra de ouro (vale para todas as etapas)

Fontes, em ordem de autoridade: `input/<p>/profile_truth.md` > `data/<p>/resume.json` > PDFs/DOCX em `input/<p>/` > `input/<p>/about_me.md`.

- Nunca invente empresa, cargo, data, tecnologia, certificação ou número. Métrica só se o número exato estiver nas fontes.
- Item em "Lacunas" ou "NÃO INCLUIR" do `profile_truth.md` nunca aparece como experiência.
- Requisito da vaga sem evidência é **lacuna**: registre, não maquie. Não suba a nota por algo sem evidência.
- Mantenha **todas** as posições de `work`, ordem cronológica reversa. Dentro de cada uma, o mais relevante para a vaga primeiro; não descarte evidência distinta só por ser menos relevante.
- Sem documentos, dados bancários ou contexto pessoal privado.

## Início: pedir só o essencial

O usuário só precisa fornecer duas coisas. Antes de qualquer etapa, confira o que já existe e peça **apenas o que falta**, numa mensagem curta:
1. **Currículo em PDF/DOCX** (e, se quiser, o PDF do LinkedIn: Mais ⋯ → Salvar como PDF). Pode vir como caminho ou arrastado no chat. Copie para `input/<p>/`. Se `input/<p>/` já tem PDF e `data/<p>/resume.json` existe, não peça de novo.
2. **A vaga**: texto colado (ou link; se for link, abra e extraia o texto).

Nome da pessoa (`<p>`): se já existe uma pasta em `input/` para ela, use essa; senão, o primeiro nome do currículo em snake_case ASCII (ex.: `guilherme`).

`profile_truth.md` (fonte de verdade da pessoa, vale para todas as vagas): não peça. Se não existir, crie um rascunho **só com fatos dos PDFs** (contato, experiências, formação, competências, idiomas) e uma seção `## ❌ NÃO INCLUIR` vazia para a pessoa preencher. Não escreva lacunas de vaga nele: as lacunas de cada vaga vão no `rating_report.md` daquela vaga. Avise o usuário para revisar o rascunho.

Com PDF e vaga em mãos, siga todas as etapas abaixo sem parar para perguntar. Dúvidas que as regras não resolvem (ex.: idioma, dado ambíguo) viram uma escolha conservadora registrada no `rating_report.md`, não uma pergunta.

## Etapa 0: base (só se `data/<p>/resume.json` não existir ou o usuário pedir para refazer)

1. Leia todos os PDF/DOCX de `input/<p>/` (com a ferramenta de leitura de arquivos que você tiver; se não ler PDF, extraia o texto com `python -c "import fitz,sys;print(''.join(p.get_text() for p in fitz.open(sys.argv[1])))" arquivo.pdf`) e o `profile_truth.md`, se houver.
2. Escreva `data/<p>/resume.json` no schema JSON Resume: `basics`, `work[{name,position,location,startDate,endDate,highlights}]`, `education`, `skills[{name,keywords}]`, `certificates`, `projects`, `languages`. Campos sem informação podem ficar vazios ou ausentes. Mantenha o texto no idioma original das fontes (a base é fiel; a tradução acontece na vaga). Datas `AAAA-MM`; emprego atual = `"Present"`. Data de fim ausente: use `"Present"` só se a fonte indicar que é o emprego atual (ex.: "– atual", o mais recente sem fim); senão deixe vazio e avise.
3. Avise que rodar de novo sobrescreve correções manuais. Peça ao usuário para revisar.

## Etapa 1: preparar

1. Vaga: texto colado pelo usuário ou `input/<p>/job_desc.md`. Salve o texto colado em `input/<p>/job_desc.md`.
2. Slug da pasta: `<cargo>_<empresa>` em snake_case ASCII, só o cargo principal, sem nível nem parênteses, até ~40 caracteres (ex.: "Senior Full-Stack Engineer (React + Node) — Example Corp" → `full_stack_engineer_example_corp`). Saída em `outputs/<p>/<slug>/` com `json/`, `evaluations/`, `latex/`, `pdf/`.
3. Idioma do currículo: o que o usuário pedir. Se ele não disser, use o idioma da **vaga** (vaga em inglês → currículo em inglês, `--lang en`; vaga em português → pt-BR) e registre a escolha no `rating_report.md`.

## Os 5 agentes

**Como rodar cada agente, conforme a ferramenta:**
- **Com subagentes** (ex.: Agent/Task tool no Claude Code, ou o recurso equivalente da sua ferramenta, se houver): cada papel é um subagente separado, na ordem abaixo. É o modo recomendado, porque o Gerente avalia sem ter escrito o currículo.
- **Sem subagentes:** faça os papéis em sequência, você mesmo. Ao trocar de papel, declare o papel novo, releia os arquivos do disco (não confie na memória do que escreveu) e, como Gerente, avalie com olhar de quem não escreveu: procure afirmações sem fonte antes de procurar qualidades.
- **Chat sem arquivos** (ChatGPT, Gemini ou Grok no navegador): use `prompts/00-prompt-unico.md` na raiz do repositório.

Você é o orquestrador: passa caminhos de arquivo (não o conteúdo), espera cada um terminar, confere o arquivo que ele gerou e chama o próximo. Todo prompt de subagente começa com a "Regra de ouro" acima copiada na íntegra, mais: pessoa `<p>`, pasta de saída, idioma, e os caminhos de `profile_truth.md`, `data/<p>/resume.json`, PDFs em `input/<p>/` e `input/<p>/job_desc.md`.

| # | Agente | Lê | Escreve |
|---|---|---|---|
| 1 | Estrategista de Carreira | fontes + vaga | `json/resume.json` (rascunho) |
| 2 | Gerente de Contratação | vaga + `json/resume.json` + fontes | `evaluations/round_N.md` terminando em `FINAL_RATING: X.X` |
| 3 | Editor de Currículo | avaliação da rodada + `json/resume.json` + fontes | `json/resume.json` revisado + `coverage_review.md` |
| 4 | Candidato | histórico de notas + avaliação final + JSON final | `rating_report.md` |
| 5 | Coach de Entrevista | vaga + JSON final | `interview_prep.md` |

### 1. Estrategista
Prompt: reposicionar o currículo para a vaga sem inventar. `summary` de 3–4 frases falando com as prioridades da vaga; `label` alinhado ao cargo sem prometer o que não tem; todas as posições mantidas, mais relevante primeiro dentro de cada uma; bullets com verbo de ação/STAR e terminologia da vaga só onde houver evidência; `skills` reordenadas sem adicionar o que a vaga cita e as fontes não mostram. Densidade de palavras-chave (ATS): extraia da vaga a lista de termos técnicos e de responsabilidade (ex.: "integração entre sistemas", "decisões técnicas", "referência técnica", "segurança de aplicações") e use cada um que for verdadeiro no `summary`, em pelo menos um bullet e em `skills` (pode nomear a skill com o termo da vaga quando for o mesmo conceito, ex.: "Integração entre Sistemas" para REST + filas). Termo que só aparece como competência listada, sem experiência que mostre uso, fica só em `skills`: não entra em bullet nem no resumo. Termo sem evidência não entra em lugar nenhum. `projects` não repete bullets da experiência palavra por palavra: descreva o problema, a solução técnica e as tecnologias. Schema igual a `data/<p>/resume.json`. Voz pt-BR: primeira pessoa no passado ("Desenvolvi", "Liderei"), nunca terceira pessoa, frases em português. Podem ficar em inglês: nomes de tecnologia, nomes de cargo oficiais (ex.: "Software Engineer", que o mercado brasileiro usa) e jargão técnico sem tradução corrente (ex.: "pull request", "deploy"). Ao traduzir um cargo, use a forma que a pessoa usa no próprio currículo; se não houver pista de gênero, mantenha o cargo original em inglês. Voz en: "Developed", "Led".

### 2 ⇄ 3. Gerente e Editor (loop, até 3 revisões)
- **Gerente** (sempre um subagente novo, que não escreveu o currículo; sem subagentes, siga a regra de troca de papel acima): avaliar como gerente de contratação crítico. Nota 1–10, 3–5 forças, 3–5 lacunas com como tratar de forma verdadeira, palavras-chave ausentes, 2–3 sugestões de apresentação. Só vale evidência escrita no currículo e sustentada pelas fontes; requisito sem evidência fica lacuna e não sobe nota. Última linha exatamente `FINAL_RATING: X.X`.
- Você lê a nota. Logo depois de cada avaliação N, guarde a versão avaliada em `json/resume_round_N.json` (inclusive a última). Se ≥ 8.5, sai do loop.
- **Editor**: aplicar o feedback no JSON sem fabricar (lacuna real continua lacuna), mesmas posições e mesma contagem de `work`, nada de métrica nova. Gera também `coverage_review.md`: por posição, temas das fontes → bullets finais, e omissões (zero de evidência profissional).
- Pare quando: nota ≥ 8.5; ou uma revisão não sobe a nota; ou 3 revisões. Restaure a versão de **melhor nota** para `json/resume.json`; em empate, fique com a mais recente.

Depois do loop, antes de renderizar, confira você mesmo o JSON: nenhum verbo em terceira pessoa ("Implementou", "Atuou"), e nomes de categoria em `skills` com no máximo ~15 caracteres (ex.: "Backend", "Mensageria e BD", "Segurança"), porque nomes longos quebram a coluna do PDF.

Renderize:
```bash
python -X utf8 <dir-da-skill>/scripts/render.py outputs/<p>/<slug>            # currículo em português
python -X utf8 <dir-da-skill>/scripts/render.py outputs/<p>/<slug> --lang en  # currículo em inglês
```
Gera `pdf/<nome>_curriculo.pdf` (layout próprio: bullets com recuo, competências em tabela, links clicáveis, metadados e rodapé com página) e `latex/<nome>_curriculo.tex` (versão editável, abre no Overleaf). `--latex` compila o PDF com `pdflatex` se a pessoa preferir esse visual. O script termina com erro se o PDF não for criado: nesse caso, leia a mensagem e corrija antes de seguir.

Controle de qualidade visual (obrigatório): converta cada página em imagem e olhe:
```bash
python -X utf8 -c "import fitz,sys;d=fitz.open(sys.argv[1]);[p.get_pixmap(dpi=80).save(f'{sys.argv[2]}/page_{i}.png') for i,p in enumerate(d)]" <pdf> <pasta-temporária>
```
(`fitz` = `pip install PyMuPDF`; se não houver, extraia o texto com `pdftotext` ou leia o PDF direto.) Corrija no JSON e renderize de novo se houver: título de seção sozinho no fim da página, página quase vazia por poucos itens (condense certificados/dados sem perder fatos), texto em inglês ou terceira pessoa, URL quebrada.

### 4. Candidato
Passe o histórico de notas que você mediu (rodada → nota, motivo da parada). Prompt: relatório curto com nota final e se bateu 8.5 exatamente como no histórico, principais melhorias, lacunas abertas e o que conferir antes de enviar. Nunca citar nota fora do histórico; ficar abaixo de 8.5 é resultado válido.

### 5. Coach de Entrevista
Prompt: guia com análise da vaga (3 must-haves); 15 perguntas (5 técnicas, 5 comportamentais, 3 situacionais, 2 motivação) com por que perguntam, resposta STAR baseada só no currículo (sem inventar métrica ou sistema; use `[substitua por um exemplo real seu]` quando faltar história) e talking points; 5 pontos a enfatizar; 2–3 red flags e como tratar; 8–10 perguntas para o entrevistador; checklist pré-entrevista; dicas de salário.

## Etapa 6: Entregar

Responda curto: caminho do PDF, nota final e se bateu 8.5, as lacunas principais da vaga, e o lembrete de que o usuário deve ler o PDF inteiro e se candidatar ele mesmo. Não se candidate nem preencha formulários por ele.
