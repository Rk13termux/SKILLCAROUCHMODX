"""Componentes extra: stack, error, timeline, index.

- stack:  fila de tecnologías (badges con color por tecnología).
- error:  consola con traceback real (error típico + su lectura).
- timeline: ruta de aprendizaje por fases/semanas.
- index:  "lo que verás en este post" (numerado).
"""

import html as _html

MAX_STACK = 8
MAX_TIMELINE = 6
MAX_INDEX = 7

# color por tecnología (código de lenguaje, mismo criterio que gh-stats)
_COLORES = {
    "python": "#3572A5", "javascript": "#F1E05A", "typescript": "#3178C6",
    "go": "#00ADD8", "rust": "#DEA584", "shell": "#89E051", "bash": "#89E051",
    "git": "#F05032", "docker": "#2496ED", "sql": "#E38C00", "html": "#E34C26",
    "css": "#563D7C", "java": "#B07219", "c": "#555555", "c++": "#F34B7D",
    "linux": "#1793D1", "k8s": "#326CE5", "aws": "#FF9900", "react": "#61DAFB",
    "flask": "#FFFFFF", "fastapi": "#009688", "django": "#092E20",
    "pytest": "#4C9F70", "pandas": "#150458", "numpy": "#4D77CF",
}


def _dot(color):
    return (f'<span class="stack__dot" style="background:{color}"></span>')


def render_stack(props, ctx, warnings=None):
    items = props.get("items") or props.get("tecnologias") or []
    titulo = str(props.get("titulo") or "").strip()
    pie = str(props.get("pie") or "").strip()
    if len(items) > MAX_STACK:
        if warnings is not None:
            warnings.append(f"stack: {len(items)} items > {MAX_STACK}, se recortan")
        items = items[:MAX_STACK]
    chips = []
    for it in items:
        if isinstance(it, str):
            it = {"v": it}
        v = str(it.get("v") or it.get("nombre") or "").strip()
        sub = str(it.get("sub") or "").strip()
        if not v:
            continue
        color = it.get("color") or _COLORES.get(v.lower(), None) or _COLORES.get(
            v.lower().split()[0], "#9CA3AF")
        chips.append(
            f'<span class="stack__chip">{_dot(str(color))}'
            f'<b>{_html.escape(v)}</b>'
            + (f'<span class="stack__sub">{_html.escape(sub)}</span>' if sub else "")
            + "</span>")
    return (
        '<div class="stack">'
        + (f'<div class="stack__titulo">{_html.escape(titulo)}</div>' if titulo else "")
        + f'<div class="stack__fila">{"".join(chips)}</div>'
        + (f'<div class="stack__pie">{_html.escape(pie)}</div>' if pie else "")
        + "</div>"
    )


def _clase_linea(ln):
    bajo = ln.strip().lower()
    if bajo.startswith("traceback"):
        return "err-head"
    if any(c in bajo for c in ("error", "exception")):
        return "err"
    if bajo.startswith("file") or ln.startswith("    "):
        return "err-ctx"
    return "err-out"


def render_error(props, ctx, warnings=None):
    titulo = str(props.get("titulo") or "").strip()
    archivo = str(props.get("archivo") or props.get("file") or "main.py").strip()
    texto = str(props.get("texto") or props.get("error") or props.get("codigo")
                or "").rstrip("\n")
    linea = str(props.get("linea") or "").strip()   # "salida" opcional
    pie = str(props.get("pie") or "").strip()
    lineas = texto.splitlines()[:12]
    filas = "".join(
        f'<div class="err__line err__line--{_clase_linea(ln)}">'
        f'{_html.escape(ln) if ln.strip() else "&nbsp;"}</div>'
        for ln in lineas)
    extra = ""
    if linea:
        extra = (f'<div class="err__resumen">{_html.escape(linea)}</div>')
    if not pie:
        pie = f"● {archivo} — error real, no inventado"
    return (
        '<div class="err">'
        '<div class="err__bar">'
        '<span class="err__dot err__dot--r"></span>'
        '<span class="err__dot err__dot--y"></span>'
        '<span class="err__dot err__dot--g"></span>'
        f'<span class="err__file">{_html.escape(archivo)}</span></div>'
        + (f'<div class="err__titulo">{_html.escape(titulo)}</div>' if titulo else "")
        + f'<div class="err__body">{filas}</div>{extra}'
        f'<div class="err__pie">{_html.escape(pie)}</div></div>'
    )


def render_timeline(props, ctx, warnings=None):
    titulo = str(props.get("titulo") or "").strip()
    etapas = props.get("etapas") or props.get("fases") or props.get("items") or []
    pie = str(props.get("pie") or "").strip()
    if len(etapas) > MAX_TIMELINE:
        if warnings is not None:
            warnings.append(f"timeline: {len(etapas)} etapas > {MAX_TIMELINE}, recortan")
        etapas = etapas[:MAX_TIMELINE]
    filas = []
    for e in etapas:
        if isinstance(e, str):
            e = {"v": e}
        v = str(e.get("v") or e.get("titulo") or "").strip()
        sub = str(e.get("sub") or e.get("detalle") or "").strip()
        estado = str(e.get("estado") or "").strip().lower()
        mark = {"ok": "✓", "run": "▶", "error": "✕"}.get(estado, "•")
        filas.append(
            f'<div class="tl__item">'
            f'<span class="tl__mark tl__mark--{estado or "idle"}">{mark}</span>'
            f'<span class="tl__txt"><b>{_html.escape(v)}</b>'
            + (f'<span class="tl__sub">{_html.escape(sub)}</span>' if sub else "")
            + "</span></div>")
    return (
        '<div class="tl">'
        + (f'<div class="tl__titulo">{_html.escape(titulo)}</div>' if titulo else "")
        + "".join(filas)
        + (f'<div class="tl__pie">{_html.escape(pie)}</div>' if pie else "")
        + "</div>"
    )


def render_index(props, ctx, warnings=None):
    titulo = str(props.get("titulo") or "Lo que verás").strip()
    items = props.get("items") or props.get("puntos") or []
    pie = str(props.get("pie") or "").strip()
    if len(items) > MAX_INDEX:
        if warnings is not None:
            warnings.append(f"index: {len(items)} items > {MAX_INDEX}, se recortan")
        items = items[:MAX_INDEX]
    filas = []
    for i, it in enumerate(items, 1):
        if isinstance(it, str):
            it = {"v": it}
        v = str(it.get("v") or it.get("titulo") or "").strip()
        n = str(it.get("n") or i)
        filas.append(
            f'<div class="idx__item"><span class="idx__n">{n}</span>'
            f'<span class="idx__v">{_html.escape(v)}</span></div>')
    return (
        '<div class="idx">'
        f'<div class="idx__titulo">{_html.escape(titulo)}</div>'
        + "".join(filas)
        + (f'<div class="idx__pie">{_html.escape(pie)}</div>' if pie else "")
        + "</div>"
    )
