"""Build an editable LaTeX resume from the JSON (compile with pdflatex, or open in Overleaf)."""
import json

from resume.latex_utils import escape_latex as esc

TITLES = {
    "pt": dict(summary="Resumo Profissional", skills="Competências", work="Experiência Profissional",
               edu="Formação Acadêmica", proj="Projetos", cert="Cursos e Certificações",
               lang="Idiomas", in_="em", present="Presente"),
    "en": dict(summary="Professional Summary", skills="Skills", work="Work Experience",
               edu="Education", proj="Projects", cert="Courses and Certifications",
               lang="Languages", in_="in", present="Present"),
}

PREAMBLE = r"""\documentclass[a4paper,11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage[usenames,dvipsnames]{color}
\usepackage{enumitem}
\usepackage[pdftex]{hyperref}
\usepackage{fancyhdr}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}
\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{\vspace{-4pt}\scshape\raggedright\large}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[1]{\item\small{#1 \vspace{-2pt}}}
\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
  \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
    \textbf{#1} & #2 \\
    \textit{\small#3} & \textit{\small #4} \\
  \end{tabular*}\vspace{-5pt}
}
\newcommand{\resumeSubItem}[2]{\item\small{\textbf{#1}: #2}\vspace{-4pt}}
\newcommand{\listStart}{\begin{itemize}[leftmargin=0em, itemindent=0em, label={}, itemsep=0ex]}
\newcommand{\listEnd}{\end{itemize}}
\newcommand{\itemsStart}{\begin{itemize}}
\newcommand{\itemsEnd}{\end{itemize}\vspace{-5pt}}
"""


def generate_latex_resume(data: dict, language: str = "pt-BR") -> str:
    T = TITLES["en" if str(language).lower().startswith("en") else "pt"]
    b = data.get("basics", {})

    def date(d):
        d = str(d or "")
        return T["present"] if d.lower() in ("present", "atual", "presente") else esc(d)

    def period(item):
        s, e = date(item.get("startDate")), date(item.get("endDate"))
        return f"{s} -- {e}" if s and e else s or e

    out = [PREAMBLE, r"\begin{document}", ""]

    # Header
    loc = b.get("location", {}) or {}
    contact = [esc(b.get("email", "")), esc(b.get("phone", "")),
               esc(", ".join(x for x in (loc.get("city"), loc.get("region")) if x))]
    for p in b.get("profiles", []):
        url = p.get("url", "")
        if url and " " not in url:
            contact.append(r"\href{" + url + "}{" + esc(url.split("//")[-1]) + "}")
    if b.get("url"):
        contact.append(r"\href{" + b["url"] + "}{" + esc(b["url"].split("//")[-1]) + "}")
    out += [r"{\Large\textbf{" + esc(b.get("name", "")) + r"}}\\",
            r"{\small " + esc(b.get("label", "")) + r"}\\",
            r"{\small " + r" $\cdot$ ".join(c for c in contact if c) + "}", ""]

    if b.get("summary"):
        out += [r"\section{" + T["summary"] + "}", r"\small{" + esc(b["summary"]) + "}", ""]

    if data.get("skills"):
        out += [r"\section{" + T["skills"] + "}", r"\listStart"]
        out += [r"\resumeSubItem{" + esc(s.get("name", "")) + "}{" + esc(", ".join(s.get("keywords", []))) + "}"
                for s in data["skills"]]
        out += [r"\listEnd", ""]

    if data.get("work"):
        out += [r"\section{" + T["work"] + "}", r"\listStart"]
        for j in data["work"]:
            out.append(r"\resumeSubheading{" + esc(j.get("name", "")) + "}{" + period(j) + "}{"
                       + esc(j.get("position", "")) + "}{" + esc(j.get("location", "")) + "}")
            if j.get("highlights"):
                out += [r"\itemsStart"] + [r"\resumeItem{" + esc(h) + "}" for h in j["highlights"]] + [r"\itemsEnd"]
        out += [r"\listEnd", ""]

    if data.get("projects"):
        out += [r"\section{" + T["proj"] + "}", r"\listStart"]
        out += [r"\resumeSubItem{" + esc(p.get("name", "")) + "}{" + esc(p.get("description", "")) + "}"
                for p in data["projects"]]
        out += [r"\listEnd", ""]

    if data.get("education"):
        out += [r"\section{" + T["edu"] + "}", r"\listStart"]
        for e in data["education"]:
            degree = " ".join(x for x in (esc(e.get("studyType", "")), T["in_"] if e.get("area") else "",
                                          esc(e.get("area", ""))) if x)
            out.append(r"\resumeSubheading{" + esc(e.get("institution", "")) + "}{" + period(e) + "}{"
                       + degree + "}{" + esc(e.get("location", "")) + "}")
        out += [r"\listEnd", ""]

    if data.get("certificates"):
        out += [r"\section{" + T["cert"] + "}", r"\listStart"]
        for c in data["certificates"]:
            extra = ", ".join(esc(x) for x in (c.get("issuer"), c.get("date")) if x)
            out.append(r"\item\small{" + esc(c.get("name", "")) + (f" ({extra})" if extra else "") + "}")
        out += [r"\listEnd", ""]

    if data.get("languages"):
        out += [r"\section{" + T["lang"] + "}", r"\small{" + r" $\cdot$ ".join(
            esc(f"{l.get('language', '')}: {l.get('fluency', '')}") for l in data["languages"]) + "}", ""]

    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


def render_resume(json_file_path, output_file_path, language="pt-BR"):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(generate_latex_resume(data, language))
