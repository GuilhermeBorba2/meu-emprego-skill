def escape_latex(text) -> str:
    """Escape LaTeX special characters."""
    special = {
        "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\^{}", "\\": r"\textbackslash{}",
    }
    return "".join(special.get(c, c) for c in str(text or ""))
