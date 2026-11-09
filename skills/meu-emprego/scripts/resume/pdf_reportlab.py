"""Clean, ATS-friendly resume PDF with reportlab (used when pdflatex is not installed)."""
import json
import os
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

ACCENT = colors.HexColor("#1a5276")
DARK = colors.HexColor("#1c1c1c")
GRAY = colors.HexColor("#555555")
LIGHT = colors.HexColor("#808080")

PAGE_W, PAGE_H = A4
MARGIN_H = 1.6 * cm
MARGIN_V = 1.3 * cm
USABLE_W = PAGE_W - 2 * MARGIN_H

FONT, BOLD, ITALIC = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
BODY = 9.2
LEAD = 12.4

LABELS = {
    "pt": dict(summary="RESUMO PROFISSIONAL", skills="COMPETÊNCIAS", work="EXPERIÊNCIA PROFISSIONAL",
               edu="FORMAÇÃO ACADÊMICA", proj="PROJETOS", cert="CURSOS E CERTIFICAÇÕES",
               lang="IDIOMAS", present="Presente", page="Página", of="de", stack="Tecnologias"),
    "en": dict(summary="PROFESSIONAL SUMMARY", skills="SKILLS", work="PROFESSIONAL EXPERIENCE",
               edu="EDUCATION", proj="PROJECTS", cert="COURSES AND CERTIFICATIONS",
               lang="LANGUAGES", present="Present", page="Page", of="of", stack="Stack"),
}
MONTHS = {
    "pt": "Jan Fev Mar Abr Mai Jun Jul Ago Set Out Nov Dez".split(),
    "en": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),
}


def _t(s) -> str:
    """Escape user text for reportlab's mini-markup."""
    return escape(str(s or "")).strip()


def _styles():
    def st(name, **kw):
        base = dict(fontName=FONT, fontSize=BODY, leading=LEAD, textColor=DARK)
        base.update(kw)
        return ParagraphStyle(name, **base)

    return {
        "name": st("name", fontName=BOLD, fontSize=20, leading=24, textColor=ACCENT),
        "label": st("label", fontSize=10.5, leading=14, textColor=GRAY),
        "contact": st("contact", fontSize=8.6, leading=12, textColor=GRAY),
        "section": st("section", fontName=BOLD, fontSize=10, leading=12, textColor=ACCENT,
                      spaceBefore=8, spaceAfter=1),
        "summary": st("summary", alignment=TA_JUSTIFY),
        "co": st("co", fontName=BOLD, fontSize=9.8, leading=12),
        "date": st("date", fontSize=8.6, leading=12, textColor=LIGHT, alignment=TA_RIGHT),
        "pos": st("pos", fontName=ITALIC, textColor=GRAY, spaceAfter=1),
        "bullet": st("bullet", leftIndent=11, bulletIndent=2, spaceAfter=1.2),
        "skill_k": st("skill_k", fontName=BOLD),
        "plain": st("plain"),
        "small": st("small", fontSize=8.4, leading=11, textColor=GRAY),
    }


def _hr():
    hr = HRFlowable(width="100%", thickness=0.6, color=ACCENT, spaceBefore=1, spaceAfter=4)
    return hr


def _section(story, S, title):
    story.append(Paragraph(title, S["section"]))
    story.append(_hr())


def _glue_sections(story):
    """Bundle each section title + rule with the first block after it."""
    out, i = [], 0
    while i < len(story):
        f = story[i]
        if isinstance(f, Paragraph) and f.style.name == "section" and i + 2 < len(story):
            nxt = story[i + 2]
            body = list(nxt._content) if isinstance(nxt, KeepTogether) else [nxt]
            out.append(KeepTogether(story[i:i + 2] + body))
            i += 3
        else:
            out.append(f)
            i += 1
    return out


def _fmt_date(d: str, lang: str) -> str:
    if not d:
        return ""
    if d.lower() in ("present", "atual", "presente"):
        return LABELS[lang]["present"]
    parts = d.split("-")
    if len(parts) >= 2 and parts[1].isdigit() and 1 <= int(parts[1]) <= 12:
        return f"{MONTHS[lang][int(parts[1]) - 1]}/{parts[0]}"
    return parts[0]


def _period(item, lang):
    start, end = _fmt_date(item.get("startDate", ""), lang), _fmt_date(item.get("endDate", ""), lang)
    return f"{start} – {end}" if start and end else start or end


def _row(left, right, S, left_w=0.72, valign="BOTTOM"):
    t = Table([[left, Paragraph(_t(right), S["date"])]],
              colWidths=[USABLE_W * left_w, USABLE_W * (1 - left_w)])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), valign),
    ]))
    return t


def _link(url: str) -> str:
    shown = url.replace("https://", "").replace("http://", "").rstrip("/")
    return f'<link href="{escape(url)}" color="#1a5276">{escape(shown)}</link>'


def generate_pdf(json_path: str, pdf_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    os.makedirs(os.path.dirname(pdf_path) or ".", exist_ok=True)

    lang = "en" if os.getenv("RESUME_LANGUAGE", "pt-BR").lower().startswith("en") else "pt"
    L, S = LABELS[lang], _styles()
    basics = data.get("basics", {})
    name = basics.get("name", "")

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT, 7.5)
        canvas.setFillColor(LIGHT)
        canvas.drawRightString(PAGE_W - MARGIN_H, MARGIN_V * 0.55,
                               f"{name} · {L['page']} {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4, leftMargin=MARGIN_H, rightMargin=MARGIN_H,
        topMargin=MARGIN_V, bottomMargin=MARGIN_V,
        title=f"{name} — {basics.get('label', '')}".strip(" —"), author=name,
        subject=basics.get("label", ""),
    )
    story = []

    # Header
    story.append(Paragraph(_t(name), S["name"]))
    if basics.get("label"):
        story.append(Paragraph(_t(basics["label"]), S["label"]))
    loc = basics.get("location", {}) or {}
    location = ", ".join(x for x in (loc.get("city"), loc.get("region")) if x)
    contact = [_t(basics.get("email")), _t(basics.get("phone")), _t(location)]
    urls = [p.get("url") for p in basics.get("profiles", []) if p.get("url") and " " not in p["url"]]
    if basics.get("url"):
        urls.append(basics["url"])
    contact += [_link(u) for u in urls]
    story.append(Paragraph("  ·  ".join(c for c in contact if c), S["contact"]))
    story.append(Spacer(1, 2))

    # Summary
    if basics.get("summary"):
        _section(story, S, L["summary"])
        story.append(Paragraph(_t(basics["summary"]), S["summary"]))

    # Skills: one row per category, fixed label column (no awkward wrapping)
    skills = [s for s in data.get("skills", []) if s.get("keywords")]
    if skills:
        _section(story, S, L["skills"])
        rows = [[Paragraph(_t(s.get("name")), S["skill_k"]),
                 Paragraph(_t(", ".join(s["keywords"])), S["plain"])] for s in skills]
        t = Table(rows, colWidths=[3.6 * cm, USABLE_W - 3.6 * cm])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 0.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
        ]))
        story.append(t)

    # Experience
    if data.get("work"):
        _section(story, S, L["work"])
        for job in data["work"]:
            co = _t(job.get("name"))
            if job.get("location"):
                co += f'  <font name="{FONT}" size="8.4" color="#808080">{_t(job["location"])}</font>'
            head = [_row(Paragraph(co, S["co"]), _period(job, lang), S)]
            if job.get("position"):
                head.append(Paragraph(_t(job["position"]), S["pos"]))
            bullets = [Paragraph(_t(h), S["bullet"], bulletText="•") for h in job.get("highlights", [])]
            # keep the header with its first two bullets
            story.append(KeepTogether(head + bullets[:2]))
            story.extend(bullets[2:])
            story.append(Spacer(1, 4))

    # Projects
    if data.get("projects"):
        _section(story, S, L["proj"])
        for p in data["projects"]:
            block = [Paragraph(f"<b>{_t(p.get('name'))}</b>"
                               + (f" — {_t(p['description'])}" if p.get("description") else ""), S["plain"])]
            block += [Paragraph(_t(h), S["bullet"], bulletText="•") for h in p.get("highlights", [])]
            if p.get("keywords"):
                block.append(Paragraph(f"<i>{L['stack']}:</i> {_t(', '.join(p['keywords']))}", S["small"]))
            story.append(KeepTogether(block + [Spacer(1, 3)]))

    # Education
    if data.get("education"):
        _section(story, S, L["edu"])
        for e in data["education"]:
            degree = " ".join(x for x in (e.get("studyType"), ("em" if lang == "pt" else "in") if e.get("area") else "", e.get("area")) if x)
            left = Paragraph(f"<b>{_t(degree)}</b> — {_t(e.get('institution'))}", S["plain"])
            story.append(_row(left, _period(e, lang) if e.get("startDate") else _fmt_date(e.get("endDate", ""), lang), S, 0.82, "TOP"))
            story.append(Spacer(1, 1.5))

    # Certificates (compact)
    certs = data.get("certificates", [])
    if certs:
        _section(story, S, L["cert"])
        for c in certs:
            extra = " · ".join(x for x in (_t(c.get("issuer")), _t(c.get("date"))) if x)
            story.append(Paragraph(_t(c.get("name")) + (f' <font color="#808080">({extra})</font>' if extra else ""),
                                   S["bullet"], bulletText="•"))

    # Languages
    if data.get("languages"):
        _section(story, S, L["lang"])
        story.append(Paragraph("  ·  ".join(
            f"<b>{_t(x.get('language'))}</b>: {_t(x.get('fluency'))}" for x in data["languages"]), S["plain"]))

    story = _glue_sections(story)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"PDF gerado: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    import sys
    generate_pdf(sys.argv[1], sys.argv[2])
