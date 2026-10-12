"""Componente terminal (CLI): comandos, salida, estados."""

import html as _html

TIPOS = {
    "cmd": "cmd",
    "out": "out",
    "ok": "ok",
    "err": "err",
    "error": "err",
    "warn": "warn",
    "warning": "warn",
    "cmt": "out",
}

PROMPTS = {"cmd": "$", "cmt": "#"}


def _linea(item):
    if isinstance(item, str):
        item = {"t": "out", "v": item}
    t = (item.get("t") or item.get("tipo") or "out").lower()
    t = TIPOS.get(t, "out")
    v = _html.escape(str(item.get("v") or item.get("texto") or ""))
    cls = f"terminal__line--{t}"
    if t == "cmd":
        prompt = _html.escape(str(item.get("prompt") or PROMPTS["cmd"]))
        return (f'<div class="terminal__line {cls}">'
                f'<span class="prompt">{prompt}</span> {v}</div>')
    if t == "cmt":
        return (f'<div class="terminal__line terminal__line--out">'
                f'<span class="cmt">{v}</span></div>')
    return f'<div class="terminal__line {cls}">{v}</div>'


def render(props, ctx, warnings=None):
    titulo = props.get("titulo") or props.get("title") or "terminal"
    lines = props.get("lines") or props.get("lineas") or []
    if not lines:
        lines = [{"t": "cmd", "v": str(props.get("cmd") or "ls -la")}]
        for k in ("out", "salida", "output"):
            if props.get(k):
                lines += [{"t": "out", "v": s}
                          for s in str(props[k]).splitlines()]
    if len(lines) > 14:
        lines = lines[:14]
        if warnings is not None:
            warnings.append("terminal: más de 14 líneas, se recortaron")
    cuerpo = "".join(_linea(x) for x in lines)
    return (
        '<div class="terminal">'
        '<div class="terminal__bar">'
        '<span class="terminal__dot terminal__dot--r"></span>'
        '<span class="terminal__dot terminal__dot--y"></span>'
        '<span class="terminal__dot terminal__dot--g"></span>'
        f'<span class="terminal__titulo">{_html.escape(titulo)}</span>'
        "</div>"
        f'<div class="terminal__body">{cuerpo}</div>'
        "</div>"
    )
