"""Render a resume JSON to PDF (and an editable .tex).

Usage:
  python -X utf8 <skill-dir>/scripts/render.py outputs/<person>/<slug> [--lang en] [--latex]
  python -X utf8 <skill-dir>/scripts/render.py caminho/resume.json    [--lang en] [--latex]

Output: pdf/<first_name>_curriculo.pdf and latex/<first_name>_curriculo.tex next to the input.
  --lang en  English section titles (default: Portuguese)
  --latex    compile the PDF with pdflatex instead of the built-in layout (needs LaTeX installed)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def file_stem(data: dict) -> str:
    """<primeiro_nome>_curriculo, from basics.name (ASCII, lowercase)."""
    name = data.get("basics", {}).get("name", "")
    first = (name.split() or ["curriculo"])[0]
    first = unicodedata.normalize("NFKD", first).encode("ascii", "ignore").decode().lower()
    first = "".join(c for c in first if c.isalnum()) or "curriculo"
    return f"{first}_curriculo"


def compile_latex(tex: Path, pdf_dir: Path) -> bool:
    if not shutil.which("pdflatex"):
        print("pdflatex não encontrado; usando o layout padrão.")
        return False
    try:
        for _ in range(2):
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(pdf_dir), str(tex)],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("pdflatex falhou; usando o layout padrão.")
        return False
    for ext in (".aux", ".log", ".out"):
        (pdf_dir / (tex.stem + ext)).unlink(missing_ok=True)
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="pasta outputs/<pessoa>/<slug> ou um arquivo resume.json")
    ap.add_argument("--lang", default="pt-BR", help="pt-BR (padrão) ou en")
    ap.add_argument("--latex", action="store_true", help="compilar com pdflatex")
    args = ap.parse_args()

    arg = Path(args.path).resolve()
    if arg.suffix.lower() == ".json":  # a resume.json saved from a web chat
        json_path, out = arg, arg.parent
    else:  # outputs/<person>/<slug> folder
        json_path, out = arg / "json" / "resume.json", arg
    if not json_path.exists():
        sys.exit(f"Arquivo não encontrado: {json_path}")
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"JSON inválido em {json_path}: {e}")

    os.environ["RESUME_LANGUAGE"] = args.lang
    from resume.generator import generate_latex_resume
    from resume.pdf_reportlab import generate_pdf

    stem = file_stem(data)
    tex_dir, pdf_dir = out / "latex", out / "pdf"
    tex_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)

    tex = tex_dir / f"{stem}.tex"
    tex.write_text(generate_latex_resume(data, args.lang), encoding="utf-8")

    pdf = pdf_dir / f"{stem}.pdf"
    if not (args.latex and compile_latex(tex, pdf_dir)):
        generate_pdf(str(json_path), str(pdf))
    if not pdf.exists():
        sys.exit(f"Falha: o PDF não foi gerado ({pdf})")
    print(f"PDF: {pdf}")
    print(f"LaTeX editável: {tex}")


if __name__ == "__main__":
    main()
