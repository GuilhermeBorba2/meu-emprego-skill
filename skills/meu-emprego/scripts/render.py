"""Render <out_dir>/json/resume.json to LaTeX + PDF.

Usage: python -X utf8 <skill-dir>/scripts/render.py outputs/<person>/<slug>
Uses pdflatex if installed; otherwise falls back to reportlab.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from resume.generator import generate  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1]).resolve()
    json_path = out / "json" / "resume.json"
    if not json_path.exists():
        sys.exit(f"Not found: {json_path}")
    (out / "latex").mkdir(parents=True, exist_ok=True)
    (out / "pdf").mkdir(parents=True, exist_ok=True)
    generate(
        json_path=str(json_path),
        latex_path=str(out / "latex" / "output_resume.tex"),
        pdf_dir=str(out / "pdf"),
    )
    print(f"PDF: {out / 'pdf' / 'output_resume.pdf'}")


if __name__ == "__main__":
    main()
