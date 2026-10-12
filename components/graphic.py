"""Infografía de pasos + checklist de takeaways."""

import html as _html

MAX_PASOS = 4
MAX_ITEMS = 4


def render_pasos(props, ctx, warnings=None):
    pasos = props.get("pasos") or props.get("steps") or []
    titulo = props.get("titulo") or props.get("title") or ""
    if len(pasos) > MAX_PASOS:
        if warnings is not None:
            warnings.append(f"pasos: {len(pasos)} > {MAX_PASOS}, se recortan")
        pasos = pasos[:MAX_PASOS]
    filas = []
    for i, p in enumerate(pasos, 1):
        if isinstance(p, str):
            p = {"t": p}
        t = _html.escape(str(p.get("t") or p.get("titulo") or ""))
        d = _html.escape(str(p.get("d") or p.get("desc") or ""))
        n = p.get("n", i)
        desc = f'<div class="paso__d">{d}</div>' if d else ""
        filas.append(
            f'<div class="paso"><div class="paso__n">{_html.escape(str(n))}</div>'
            f'<div><div class="paso__t">{t}</div>{desc}</div></div>'
        )
    titulo_html = (f'<div class="pasos__titulo">{_html.escape(str(titulo))}</div>'
                   if titulo else "")
    return f'<div class="pasos">{titulo_html}{"".join(filas)}</div>'


def render_checklist(props, ctx, warnings=None):
    items = props.get("items") or props.get("lista") or []
    titulo = props.get("titulo") or props.get("title") or "Takeaways"
    if len(items) > MAX_ITEMS:
        if warnings is not None:
            warnings.append(f"checklist: {len(items)} > {MAX_ITEMS}, se recortan")
        items = items[:MAX_ITEMS]
    filas = []
    for it in items:
        if isinstance(it, str):
            it = {"v": it}
        texto = _html.escape(str(it.get("v") or it.get("texto") or ""))
        filas.append(f'<div class="checklist__item">'
                     f'<span class="checklist__ico">✓</span><span>{texto}</span></div>')
    return (f'<div class="checklist">'
            f'<div class="checklist__titulo">{_html.escape(str(titulo))}</div>'
            f'{"".join(filas)}</div>')
